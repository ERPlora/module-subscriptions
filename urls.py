from django.urls import path
from . import views

app_name = 'subscriptions'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Plan
    path('plans/', views.plans_list, name='plans_list'),
    path('plans/add/', views.plan_add, name='plan_add'),
    path('plans/<uuid:pk>/edit/', views.plan_edit, name='plan_edit'),
    path('plans/<uuid:pk>/delete/', views.plan_delete, name='plan_delete'),
    path('plans/<uuid:pk>/toggle/', views.plan_toggle_status, name='plan_toggle_status'),
    path('plans/bulk/', views.plans_bulk_action, name='plans_bulk_action'),

    # Settings
    path('settings/', views.settings_view, name='settings'),
]
