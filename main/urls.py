from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('generate_qr_code/', views.generate_qr_code, name='generate_qr_code'),
    path('login/', views.login_view, name='login'),
    path('verify_otp_login/', views.verify_otp_login, name='verify_otp_login'),
    path('show_qr_code/', views.show_qr_code, name='show_qr_code'),
]
