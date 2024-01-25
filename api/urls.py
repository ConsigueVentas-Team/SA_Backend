from django.urls import path, include
from api import views

urlpatterns = [
    #--------- AUTHENTICATIONS URLs ---------#
    # path('auth/register',views.UserRegisterView.as_view(),name="user_register"),#Registrar un usuario
  
    #--------- JUSTIFICATION_STATUS URLs ---------#
    path('justification_status', views.JustificationStatusListCreateView.as_view(), name='justification_status_list'),
    path('justification_status/create', views.JustificationStatusListCreateView.as_view(), name='justification_status_create'),
    path('justification_status/<int:pk>', views.JustificationStatusRetrieveUpdateDestroyView.as_view(), name='justification_status_detail'),
    path('justification_status/update/<int:pk>', views.JustificationStatusRetrieveUpdateDestroyView.as_view(), name='justification_status_update'),
    path('justification_status/delete/<int:pk>', views.JustificationStatusRetrieveUpdateDestroyView.as_view(), name='justification_status_delete'),

    #--------- JUSTIFICATION URLs ---------#
    path('justification', views.JustificationListCreateView.as_view(), name='justification_list'),
    path('justification/create', views.JustificationListCreateView.as_view(), name='justification_create'),
    path('justification/<int:pk>', views.JustificationListCreateView.as_view(), name='justification_detail'),
    path('justification/update/<int:pk>', views.JustificationRetrieveUpdateDestroyView.as_view(), name='justification_update'),
    path('justification/delete/<int:pk>', views.JustificationRetrieveUpdateDestroyView.as_view(), name='justification_delete')

]