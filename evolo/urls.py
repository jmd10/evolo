from django.contrib import admin
from django.urls import path
from evolo import views
from django.contrib.auth import views as auth_views


app_name = 'evolo'
urlpatterns = [
    path('newuser',views.NewUserRegistrationView.as_view(),name='new_registration'),  # new user registration
    path('', auth_views.LoginView.as_view(template_name='registration/login.html'),name='login_view'),
    # VariableMaster
    path('home',views.Home.as_view(),name='home_view'),  #home view
    path('varmaster',views.CreateVariables.as_view(),name='var_create_view'),
    path('varupdate/<int:pk>', views.VariablesUpdate.as_view(), name='var_update'),
    # VariableResults
    path('resultsadd',views.add_results,name='add_results_view'),
    path('resultslist',views.VariableResultsList.as_view(),name= 'list_results_view'),


]
