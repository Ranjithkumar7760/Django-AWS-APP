from django.urls import path
from . import views
from .views import dashboard, user_login, user_logout, user_signup, create_patient, update_patient, delete_patient

urlpatterns = [
    path('', views.dashboard, name='dashboard'),  # Dashboard page
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('signup/', views.user_signup, name='signup'),

    # ✅ Add this route for creating a patient
    path('create/', views.create_patient, name='create_patient'),
    path('update/<int:pk>/', update_patient, name='update_patient'),
    path('delete/<int:pk>/', delete_patient, name='delete_patient'),
]
