from django.contrib import admin

from .models import Plan, Subscription

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'billing_period', 'is_active', 'created_at']
    search_fields = ['name', 'billing_period', 'description']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['plan', 'customer_name', 'customer_email', 'status', 'start_date', 'created_at']
    search_fields = ['customer_name', 'customer_email', 'status']
    readonly_fields = ['created_at', 'updated_at']

