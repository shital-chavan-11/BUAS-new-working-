
from django.urls import path
from .views import register_view, index_view, logout_view,login_view,verify_otp_view,resend_otp_view ,dashboard_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/',login_view,  name='login'),  # Use built-in login view
    path('', index_view, name='index'),
    path('logout/', logout_view, name='logout'),
    path('verify-otp/<int:user_id>/', verify_otp_view, name='verify_otp'), 
    path('resend-otp/<int:user_id>/', resend_otp_view, name='resend_otp'),
    path('dashboard/', dashboard_view, name='dashboard'),
]