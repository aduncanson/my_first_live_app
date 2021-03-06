from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from . import ajax_datatable_views

urlpatterns = [
    # Login urls
	path('register/', views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"),  
	path('logout/', views.logoutUser, name="logout"),

    # Default home pages, depending on role
    path('', views.dashboard, name="dashboard"),
    path('agent/<str:pk>/', views.agentPage, name="agent_page"),

    # Agent setting
    path('agent_settings/', views.agentSettings, name="agent_settings"),

    # Show list of all agents
    path('agent_list/', views.agentList, name="agent_list"),

    # Agent activity views
    path('agent_activity/', views.agentActivity, name="agent_activity"),
    path('agent_activity/<str:pk>/', views.agentActivity, name="agent_activity"),

    # Password reset process views
    path("reset_password/", auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"), name="reset_password"),
    path("reset_password_sent/", auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"), name="password_reset_confirm"),
    path("reset_password_complete/", auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"), name="password_reset_complete"),

    # ajax datatables
    path('ajax_datatable/agent_list/', ajax_datatable_views.AgentListAjaxDatatableView.as_view(), name="ajax_list_of_agents_table"),

]