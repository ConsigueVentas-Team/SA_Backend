from django.urls import path, include
from api import views

urlpatterns = [
    #--------- AUTHENTICATIONS URLs ---------#
    # path('auth/register',views.UserRegisterView.as_view(),name="user_register"),#Registrar un usuario

    #--------- JUSTIFICATION URLs ---------#
    path('justification/list', views.JustificationListCreateView.as_view(), name='get_justification'),
    path('justification/create', views.JustificationListCreateView.as_view(), name='create_justification'),

    path('register',views.UserRegisterView.as_view(),name="user_register"),#Registrar un usuario
    path('login',views.UserLoginView.as_view(),name="user_login"),#login
    path('profile',views.UserProfileView.as_view(),name="user_user"),#Datos del usuario authenticado
    
    # ------- PASSWORD RESET URLs ----------#
    path('changepassword',views.UserChangePasswordView.as_view(),name="user_changepassword"),#Cambiar la contraseña
    path('forgotpassword/',include('django_rest_passwordreset.urls'),name="user_forgotpassword"),#Recuperar la contraseña

    # -------- POSITION URLs -------------#
    path('position/list',views.PositionListCreateView.as_view(),name="position-list"), 
    
    # -------- DEPARTMENT URLs -------------#
    path('department/list',views.DepartmentListCreateView.as_view(),name="department-list"),

     # -------- CORE URLs -------------#
    path('core/list',views.CoreListCreateView.as_view(),name="core-list"),
    
    #---------- Schedules URLs -----------#
    path('schedule/create', views.ScheduleListCreateView.as_view(), name="schedule-create"),

    path('notification/list', views.NotificationListCreateView.as_view(), name="notification-list"),

    path('evaluation/list', views.EvaluationListCreateView.as_view(), name="evaluation-list"),

]