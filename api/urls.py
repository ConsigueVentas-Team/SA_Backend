from django.urls import path, include
from api import views

urlpatterns = [
    #--------- AUTHENTICATIONS URLs ---------#
    # path('auth/register',views.UserRegisterView.as_view(),name="user_register"),#Registrar un usuario

    #--------- JUSTIFICATION URLs ---------#
    path('justification/list', views.JustificationListView.as_view(), name='get_justification'), 
    path('justification/create', views.JustificationCreateView.as_view(), name='create_justification'),
    path('justification/accept/<int:pk>', views.JustificationRetrieveAcceptView.as_view(), name='accept_justification'),
    path('justification/decline/<int:pk>', views.JustificationRetrieveDeclineView.as_view(), name='decline_justification'),
    path('justification/delete/<int:pk>', views.JustificationDestroyView.as_view(), name='destroy_justification'),

    path('justification/search', views.JustificationSearchView.as_view(), name='justification_search'),
    
    # ------- AUTHENTICATION URLs ----------#
    path('register',views.UserRegisterView.as_view(),name="user_register"),#Registrar un usuario
    path('login',views.UserLoginView.as_view(),name="user_login"),#login
    path('profile',views.UserProfileView.as_view(),name="user_user"),#Datos del usuario authenticado

    # ------- PASSWORD RESET URLs ----------#
    path('changepassword',views.UserChangePasswordView.as_view(),name="user_changepassword"),#Cambiar la contraseña
    path('forgotpassword/',include('django_rest_passwordreset.urls'),name="user_forgotpassword"),#Recuperar la contraseña
    
    # ------- USERS URLs ----------#
    path('users/list',views.UserListView.as_view(),name="user_list"),
    path('users/<int:id>',views.UserDetailsView.as_view(),name="user_details"),
    path('users/<int:id>/update',views.UserUpdateView.as_view(),name="user_update"),

    # ------- BIRTHDAYS URLs ----------#
    path('birthday/details',views.UserBirthdayDetailsView.as_view(),name="birthday_details"),
    path('birthday/nextBirthday',views.UserNextBirthdayView.as_view(),name="birthday_details"),

    # -------- POSITION URLs -------------#
    path('position/list',views.PositionListView.as_view(),name="position-list"), 
    path('position/create',views.PositionCreateView.as_view(),name="position-create"),
    path('position/update/<int:id>',views.PositionDetailsUpdateDestroy.as_view(),name="position-update"),
    path('position/delete/<int:id>',views.PositionDetailsUpdateDestroy.as_view(),name="position-delete"),
    path('position/details/<int:id>',views.PositionDetailsUpdateDestroy.as_view(),name="position-details"),

    # -------- DEPARTMENT URLs -------------#
    path('departments/list',views.DepartmentListCreateView.as_view(),name="department-list"),
    path('departments/create',views.DepartmentListCreateView.as_view(),name="department-create"),
    path('departments/update/<int:id>',views.DepartmentDetailsUpdateDestroy.as_view(),name="department-update"),
    path('departments/delete/<int:id>',views.DepartmentDetailsUpdateDestroy.as_view(),name="department-delete"),
    path('departments/details/<int:id>',views.DepartmentDetailsUpdateDestroy.as_view(),name="department-details"),
    path('departments/statistics', views.DepartmentStatisticsView.as_view(), name="department-statistics"),
    
    # -------- CORE URLs -------------#
    path('cores/list',views.CoreListView.as_view(),name="core-list"),
    path('cores/create',views.CoreCreateView.as_view(),name="core-create"),
    path('cores/update/<int:id>',views.CoreDetailsUpdateDestroy.as_view(),name="core-update"),
    path('cores/delete/<int:id>',views.CoreDetailsUpdateDestroy.as_view(),name="core-delete"),
    path('cores/details/<int:id>',views.CoreDetailsUpdateDestroy.as_view(),name="core-details"),
    path('cores/statistics', views.CoreStatisticsView.as_view(), name="core-statistics"),
    
    #---------- SCHEDULE URLs -----------#
    path('schedule/list',views.ScheduleListCreateView.as_view(),name="schedule-list"),
    path('schedule/create', views.ScheduleListCreateView.as_view(), name="schedule-create"),
    path('schedule/<int:id>',views.ScheduleListByUserView.as_view(),name="schedule-detail"),

    #---------- NOTIFICATION URLs -----------#
    path('notification/list', views.NotificationListCreateView.as_view(), name="notification-list"),
    path('notification/create', views.NotificationListCreateView.as_view(), name="notification-create"),
    path('notification/update/<int:pk>', views.NotificationDetailView.as_view(), name="notification-update"),
    path('notification/delete/<int:pk>', views.NotificationDetailView.as_view(), name="notification-delete"),
    path('notification/details/<int:pk>', views.NotificationDetailView.as_view(), name="notification-details"),

    #---------- EVALUATION URLs -----------#
    path('evaluation/list', views.EvaluationListCreateView.as_view(), name="evaluation-list"),
    path('evaluation/create', views.EvaluationListCreateView.as_view(), name="evaluation-create"),
    path('evaluation/notes/<int:id>', views.EvaluationRetrieveUpdateView.as_view(), name="evaluation-store"),

    #---------- ATTENDANCE URLs -----------#
    path('attendance/list', views.AttendanceList.as_view(), name="attendance-list"),
    path('attendance/id', views.AttendanceByID.as_view(), name="attendance-id-list"),
    path('attendance/create', views.AttendanceCreateAPIView.as_view(), name="attendance-create"),
    
    #---------- REPORTS URLs -----------#
    path('reports/list', views.ReportListAPIView.as_view(), name='get_reports'),
]
