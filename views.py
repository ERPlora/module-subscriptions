"""
Subscriptions & Memberships Module Views
"""
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404, render as django_render
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST

from apps.accounts.decorators import login_required, permission_required
from apps.core.htmx import htmx_view
from apps.core.services import export_to_csv, export_to_excel
from apps.modules_runtime.navigation import with_module_nav

from .models import Plan, Subscription

PER_PAGE_CHOICES = [10, 25, 50, 100]


# ======================================================================
# Dashboard
# ======================================================================

@login_required
@with_module_nav('subscriptions', 'dashboard')
@htmx_view('subscriptions/pages/index.html', 'subscriptions/partials/dashboard_content.html')
def dashboard(request):
    hub_id = request.session.get('hub_id')
    return {
        'total_plans': Plan.objects.filter(hub_id=hub_id, is_deleted=False).count(),
    }


# ======================================================================
# Plan
# ======================================================================

PLAN_SORT_FIELDS = {
    'name': 'name',
    'billing_period': 'billing_period',
    'is_active': 'is_active',
    'price': 'price',
    'description': 'description',
    'created_at': 'created_at',
}

def _build_plans_context(hub_id, per_page=10):
    qs = Plan.objects.filter(hub_id=hub_id, is_deleted=False).order_by('name')
    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(1)
    return {
        'plans': page_obj,
        'page_obj': page_obj,
        'search_query': '',
        'sort_field': 'name',
        'sort_dir': 'asc',
        'current_view': 'table',
        'per_page': per_page,
    }

def _render_plans_list(request, hub_id, per_page=10):
    ctx = _build_plans_context(hub_id, per_page)
    return django_render(request, 'subscriptions/partials/plans_list.html', ctx)

@login_required
@with_module_nav('subscriptions', 'plans')
@htmx_view('subscriptions/pages/plans.html', 'subscriptions/partials/plans_content.html')
def plans_list(request):
    hub_id = request.session.get('hub_id')
    search_query = request.GET.get('q', '').strip()
    sort_field = request.GET.get('sort', 'name')
    sort_dir = request.GET.get('dir', 'asc')
    page_number = request.GET.get('page', 1)
    current_view = request.GET.get('view', 'table')
    per_page = int(request.GET.get('per_page', 10))
    if per_page not in PER_PAGE_CHOICES:
        per_page = 10

    qs = Plan.objects.filter(hub_id=hub_id, is_deleted=False)

    if search_query:
        qs = qs.filter(Q(name__icontains=search_query) | Q(billing_period__icontains=search_query) | Q(description__icontains=search_query))

    order_by = PLAN_SORT_FIELDS.get(sort_field, 'name')
    if sort_dir == 'desc':
        order_by = f'-{order_by}'
    qs = qs.order_by(order_by)

    export_format = request.GET.get('export')
    if export_format in ('csv', 'excel'):
        fields = ['name', 'billing_period', 'is_active', 'price', 'description']
        headers = ['Name', 'Billing Period', 'Is Active', 'Price', 'Description']
        if export_format == 'csv':
            return export_to_csv(qs, fields=fields, headers=headers, filename='plans.csv')
        return export_to_excel(qs, fields=fields, headers=headers, filename='plans.xlsx')

    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(page_number)

    if request.htmx and request.htmx.target == 'datatable-body':
        return django_render(request, 'subscriptions/partials/plans_list.html', {
            'plans': page_obj, 'page_obj': page_obj,
            'search_query': search_query, 'sort_field': sort_field,
            'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
        })

    return {
        'plans': page_obj, 'page_obj': page_obj,
        'search_query': search_query, 'sort_field': sort_field,
        'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
    }

@login_required
def plan_add(request):
    hub_id = request.session.get('hub_id')
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        price = request.POST.get('price', '0') or '0'
        billing_period = request.POST.get('billing_period', '').strip()
        description = request.POST.get('description', '').strip()
        is_active = request.POST.get('is_active') == 'on'
        obj = Plan(hub_id=hub_id)
        obj.name = name
        obj.price = price
        obj.billing_period = billing_period
        obj.description = description
        obj.is_active = is_active
        obj.save()
        return _render_plans_list(request, hub_id)
    return django_render(request, 'subscriptions/partials/panel_plan_add.html', {})

@login_required
def plan_edit(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(Plan, pk=pk, hub_id=hub_id, is_deleted=False)
    if request.method == 'POST':
        obj.name = request.POST.get('name', '').strip()
        obj.price = request.POST.get('price', '0') or '0'
        obj.billing_period = request.POST.get('billing_period', '').strip()
        obj.description = request.POST.get('description', '').strip()
        obj.is_active = request.POST.get('is_active') == 'on'
        obj.save()
        return _render_plans_list(request, hub_id)
    return django_render(request, 'subscriptions/partials/panel_plan_edit.html', {'obj': obj})

@login_required
@require_POST
def plan_delete(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(Plan, pk=pk, hub_id=hub_id, is_deleted=False)
    obj.is_deleted = True
    obj.deleted_at = timezone.now()
    obj.save(update_fields=['is_deleted', 'deleted_at', 'updated_at'])
    return _render_plans_list(request, hub_id)

@login_required
@require_POST
def plan_toggle_status(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(Plan, pk=pk, hub_id=hub_id, is_deleted=False)
    obj.is_active = not obj.is_active
    obj.save(update_fields=['is_active', 'updated_at'])
    return _render_plans_list(request, hub_id)

@login_required
@require_POST
def plans_bulk_action(request):
    hub_id = request.session.get('hub_id')
    ids = [i.strip() for i in request.POST.get('ids', '').split(',') if i.strip()]
    action = request.POST.get('action', '')
    qs = Plan.objects.filter(hub_id=hub_id, is_deleted=False, id__in=ids)
    if action == 'activate':
        qs.update(is_active=True)
    elif action == 'deactivate':
        qs.update(is_active=False)
    elif action == 'delete':
        qs.update(is_deleted=True, deleted_at=timezone.now())
    return _render_plans_list(request, hub_id)


@login_required
@permission_required('subscriptions.manage_settings')
@with_module_nav('subscriptions', 'settings')
@htmx_view('subscriptions/pages/settings.html', 'subscriptions/partials/settings_content.html')
def settings_view(request):
    return {}

