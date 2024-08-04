from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("sign_up/", views.sign_up, name="sign_up"),
    path("home/", views.home, name="home"),
    path('legal_entities/new/', views.legal_entities_create, name='legal_entities_create'),
    path('legal_entities/list/', views.legal_entities_list, name='legal_entities_list'),
    path('partner/new/', views.partner_create, name='partner_create'),
    path('partner/list/', views.partner_list, name='partner_list'),
]
