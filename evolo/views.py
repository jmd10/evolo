from django.http import HttpResponse
from django.shortcuts import render,HttpResponseRedirect
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView,UpdateView,FormView
from django.views.generic.list import ListView
from .models import VariableMaster, VariableResults
from .forms import VariableMasterForm,VariableResultsForm,NewUserForm
from django.urls import reverse_lazy
import datetime
from django.forms import modelformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


class Home(LoginRequiredMixin,ListView):
    """display list of varibales being trcked by a particular user on the Home Page"""
    model = VariableMaster
    template_name = 'evolo/home.html'

    def get_queryset(self):
        qs = VariableMaster.objects.filter(person=self.request.user)
        return qs


class CreateVariables(LoginRequiredMixin,CreateView):
    """add variable for tracking"""
    form_class = VariableMasterForm
    template_name = "evolo/variablemaster_form.html"
    success_url = reverse_lazy('evolo:home_view')

    def get_initial(self):
        data = {'person': self.request.user}
        return data


class VariablesUpdate(LoginRequiredMixin,UpdateView):
    model = VariableMaster
    form_class = VariableMasterForm
    template_name = "evolo/variablemaster_form.html"
    success_url = reverse_lazy('evolo:home_view')


@login_required
def add_results(request):
    """function to add results for a specific date"""
    py_dt_tm = None
    if request.method == 'GET':
        user_input_dt = request.GET.get("results_date")
        py_dt_tm = datetime.datetime.strptime(user_input_dt, "%Y-%m-%d")
        record_status = VariableResults.objects.filter(variable__person=request.user, result_date=py_dt_tm.date()).exists()
        if not record_status:
            """create records in results table when the user first selects a particular date"""
            variable_obj_list = VariableMaster.objects.filter(person=request.user)
            rec_list = [VariableResults(variable=track_var, result_date=py_dt_tm) for track_var in variable_obj_list]
            VariableResults.objects.bulk_create(rec_list)

    VariableFormset = modelformset_factory(VariableResults, form=VariableResultsForm,extra=0)

    if request.method == 'POST':
        formset = VariableFormset(request.POST)
        if formset.is_valid():
            formset.save()
            messages.success(request, 'Results added/ Updated.')
            return HttpResponseRedirect(reverse_lazy('evolo:list_results_view'))
        else:
            print('formset invalid')
            print(formset.errors)
    else:
        formset = VariableFormset(
            queryset=VariableResults.objects.filter(variable__person=request.user, result_date=py_dt_tm.date()))
    return render(request, 'evolo/add_results.html', {'formset': formset})


class VariableResultsList(LoginRequiredMixin,ListView):
    """display variable results entered by the user"""
    model = VariableResults

    def get_queryset(self):
        qs = VariableResults.objects.filter(variable__person=self.request.user)
        return qs


# -----------New User Registration------------------------------------------------------------------------------
class NewUserRegistrationView(FormView):
    form_class = NewUserForm
    # form_class = UserCreationForm
    template_name = "evolo/user_registration.html"
    success_url = reverse_lazy('evolo:login_view')

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        messages.success(self.request,f"User-  {username} Created")
        return HttpResponseRedirect(reverse_lazy('evolo:login_view'))
