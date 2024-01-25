from django.urls import path, include
from api import views

urlpatterns = [
    #--------- AUTHENTICATIONS URLs ---------#
    # path('auth/register',views.UserRegisterView.as_view(),name="user_register"),#Registrar un usuario

    #--------- JUSTIFICATION URLs ---------#
    path('justification/list', views.JustificationListCreateView.as_view(), name='get_justification'),
    path('justification/create', views.JustificationListCreateView.as_view(), name='create_justification'),
    path('justification/<int:pk>', views.JustificationListCreateView.as_view(), name='justification_detail'),
    path('justification/update/<int:pk>', views.JustificationRetrieveUpdateDestroyView.as_view(), name='justification_update'),
    path('justification/delete/<int:pk>', views.JustificationRetrieveUpdateDestroyView.as_view(), name='justification_delete')

]