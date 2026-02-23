from django.urls import path
from . import views

app_name = 'subscriptions'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('plans/', views.plans, name='plans'),
    path('subscriptions/', views.subscriptions, name='subscriptions'),
    path('settings/', views.settings, name='settings'),
]
