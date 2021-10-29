from django.http import HttpResponse
from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, FormView, DeleteView
from django.views.generic.list import ListView
from .models import VariableMaster, VariableResults
from .forms import VariableMasterForm, VariableResultsForm, NewUserForm
from django.urls import reverse_lazy
import datetime
from django.forms import modelformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.


class Home(LoginRequiredMixin, ListView):
    """display list of varibales being trcked by a particular user on the Home Page"""
    model = VariableMaster
    template_name = 'evolo/home.html'

    def get_queryset(self):
        qs = VariableMaster.objects.filter(person=self.request.user)
        return qs


class CreateVariables(LoginRequiredMixin, CreateView):
    """add variable for tracking"""
    form_class = VariableMasterForm
    template_name = "evolo/variablemaster_form.html"
    success_url = reverse_lazy('evolo:home_view')

    def get_initial(self):
        data = {'person': self.request.user}
        return data


class VariablesUpdate(LoginRequiredMixin, UpdateView):
    model = VariableMaster
    form_class = VariableMasterForm
    template_name = "evolo/variablemaster_form.html"
    success_url = reverse_lazy('evolo:home_view')


@login_required
def add_results(request):
    """function to add results for a specific date"""

    if request.method == 'GET':
        record_status = VariableResults.objects.filter(variable__person=request.user,
                                                       result_date=None).exists()
        if not record_status:  # create records in results table with None values
            variable_obj_list = VariableMaster.objects.filter(person=request.user)
            rec_list = [VariableResults(variable=track_var) for track_var in variable_obj_list]
            VariableResults.objects.bulk_create(rec_list)

    VariableFormset = modelformset_factory(VariableResults, form=VariableResultsForm, extra=0)

    if request.method == 'POST':
        formset = VariableFormset(request.POST)
        user_input_dt = request.POST['results_date']  # get the user selected date
        py_user_input_dt = datetime.datetime.strptime(user_input_dt, "%Y-%m-%d")
        previous_rec = VariableResults.objects.filter(variable__person=request.user,
                                                      result_date=py_user_input_dt.date()).exists()
        if previous_rec:  # user has already entered results for this date
            messages.warning(request, f'NOT saved - Results already added for {py_user_input_dt.strftime("%d %b %y")}')
        else:  # save the results
            if formset.is_valid():
                formset.save()
                # update date in the databse , as default date in the object is None
                VariableResults.objects.filter(variable__person=request.user, result_date=None
                                               ).update(result_date=py_user_input_dt.date())

                messages.success(request, 'Results added.')
                return HttpResponseRedirect(reverse_lazy('evolo:list_results_view'))
    else:
        formset = VariableFormset(
            queryset=VariableResults.objects.filter(variable__person=request.user, result_date=None))

    return render(request, 'evolo/add_results.html', {'formset': formset})


def modify_results(request, dt):
    """modify existing results"""
    VariableFormset = modelformset_factory(VariableResults, form=VariableResultsForm, extra=0)
    formset = VariableFormset(request.POST or None,
                              queryset=VariableResults.objects.filter(variable__person=request.user, result_date=dt))
    if request.method == 'POST':
        if formset.is_valid():
            formset.save()
            messages.success(request, 'Results Updated.')
            return HttpResponseRedirect(reverse_lazy('evolo:list_results_view'))

    return render(request, 'evolo/modify_results.html', {'formset': formset})


class VariableResultsList(LoginRequiredMixin, ListView):
    """display variable results entered by the user"""
    model = VariableResults

    def get_queryset(self):
        qs = VariableResults.objects.filter(variable__person=self.request.user,result_date__isnull=False)
        return qs


def delete_variable_results(request, dt):
    """delete exeisting results from the databse"""
    tmp_dt = None
    if dt != 'None':
        try:  # if date is changed in url
            tmp_dt = datetime.datetime.strptime(dt, "%Y-%m-%d").date()
        except:
            messages.warning(request, "Date is invalid")
            return HttpResponseRedirect(reverse_lazy('evolo:list_results_view'))
        else:
            delete_qs = VariableResults.objects.filter(variable__person=request.user, result_date=dt)
    else:
        delete_qs = VariableResults.objects.filter(variable__person=request.user, result_date__isnull=True)

    if request.method == 'POST':
        if request.POST.get('btn_confirm') == 'confirm':
            delete_qs.delete()
            messages.success(request, "Results Deleted")
        else:
            pass
        return HttpResponseRedirect(reverse_lazy('evolo:list_results_view'))

    return render(request, 'evolo/confirm_delete.html', {'del_date': tmp_dt})


# -----------New User Registration------------------------------------------------------------------------------
class NewUserRegistrationView(FormView):
    form_class = NewUserForm
    # form_class = UserCreationForm
    template_name = "evolo/user_registration.html"
    success_url = reverse_lazy('evolo:login_view')

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        messages.success(self.request, f"User-  {username} Created")
        return HttpResponseRedirect(reverse_lazy('evolo:login_view'))
