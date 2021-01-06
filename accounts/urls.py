from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from . import ajax_datatable_views

urlpatterns = [
	path('register/', views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"),  
	path('logout/', views.logoutUser, name="logout"),

    path('', views.dashboard, name="dashboard"),
    path('agent/<str:pk>/', views.agentPage, name="agent_page"),

    path('agent_settings/', views.agentSettings, name="agent_settings"),

    path('agent_list/', views.agentList, name="agent_list"),

    path("reset_password/", auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"), name="reset_password"),
    path("reset_password_sent/", auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"), name="password_reset_confirm"),
    path("reset_password_complete/", auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"), name="password_reset_complete"),

    # ajax
    path('ajax_datatable/agent_list/', ajax_datatable_views.AgentListAjaxDatatableView.as_view(), name="ajax_list_of_agents_table"),

]