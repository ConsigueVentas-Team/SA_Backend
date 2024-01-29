from django.urls import path, include
from api import views

urlpatterns = [
    
    # ------- AUTHENTICATION URLs ----------#
    path('register',views.UserRegisterView.as_view(),name="user_register"),#Registrar un usuario
    path('login',views.UserLoginView.as_view(),name="user_login"),#login
    path('profile',views.UserProfileView.as_view(),name="user_user"),#Datos del usuario authenticado
    
    # ------- PASSWORD RESET URLs ----------#
    path('changepassword',views.UserChangePasswordView.as_view(),name="user_changepassword"),#Cambiar la contraseña
    path('forgotpassword/',include('django_rest_passwordreset.urls'),name="user_forgotpassword"),#Recuperar la contraseña

    #--------- JUSTIFICATION URLs ---------#
    path('justification/list', views.JustificationListCreateView.as_view(), name='get_justification'),
    path('justification/create', views.JustificationListCreateView.as_view(), name='create_justification'),

    # -------- POSITION URLs -------------#
    path('position/list',views.PositionListCreateView.as_view(),name="position-list"), 
    path('position/create',views.PositionListCreateView.as_view(),name="position-create"),
    path('position/update/<int:id>',views.PositionDetailsUpdateDestroy.as_view(),name="position-update"),
    path('position/delete/<int:id>',views.PositionDetailsUpdateDestroy.as_view(),name="position-delete"),
    path('position/details/<int:id>',views.PositionDetailsUpdateDestroy.as_view(),name="position-details"),

    # -------- DEPARTMENT URLs -------------#
    path('department/list',views.DepartmentListCreateView.as_view(),name="department-list"),
    path('department/create',views.DepartmentListCreateView.as_view(),name="department-create"),
    path('department/update/<int:id>',views.DepartmentDetailsUpdateDestroy.as_view(),name="department-update"),
    path('department/delete/<int:id>',views.DepartmentDetailsUpdateDestroy.as_view(),name="department-delete"),
    path('department/details/<int:id>',views.DepartmentDetailsUpdateDestroy.as_view(),name="department-details"),

    # -------- CORE URLs -------------#
    path('core/list',views.CoreListCreateView.as_view(),name="core-list"),
    path('core/create',views.CoreListCreateView.as_view(),name="core-create"),
    path('core/update/<int:id>',views.CoreDetailsUpdateDestroy.as_view(),name="core-update"),
    path('core/delete/<int:id>',views.CoreDetailsUpdateDestroy.as_view(),name="core-delete"),
    path('core/details/<int:id>',views.CoreDetailsUpdateDestroy.as_view(),name="core-details"),
    
    #---------- SCHEDULE URLs -----------#
    path('schedule/list',views.ScheduleListCreateView.as_view(),name="schedule-list"),
    path('schedule/create', views.ScheduleListCreateView.as_view(), name="schedule-create"),
    path('schedule/<int:id>',views.ScheduleListByUserView.as_view(),name="schedule-detail"),

    #---------- NOTIFICATION URLs -----------#
    path('notification/list', views.NotificationListCreateView.as_view(), name="notification-list"),

    #---------- EVALUATION URLs -----------#
    path('evaluation/list', views.EvaluationListCreateView.as_view(), name="evaluation-list"),
    
    #---------- ATTENDANCE URLs -----------#
    path('attendance/list', views.AttendanceList.as_view(), name="attendance-list"),
    path('attendance/id', views.AttendanceByID.as_view(), name="attendance-id-list"),
    path('attendance/create', views.AttendanceCreateAPIView.as_view(), name="attendance-create"),
]
