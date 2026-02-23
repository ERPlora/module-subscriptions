"""
Subscriptions & Memberships Module Views
"""
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from apps.accounts.decorators import login_required
from apps.core.htmx import htmx_view
from apps.modules_runtime.navigation import with_module_nav


@login_required
@with_module_nav('subscriptions', 'dashboard')
@htmx_view('subscriptions/pages/dashboard.html', 'subscriptions/partials/dashboard_content.html')
def dashboard(request):
    """Dashboard view."""
    hub_id = request.session.get('hub_id')
    return {}


@login_required
@with_module_nav('subscriptions', 'plans')
@htmx_view('subscriptions/pages/plans.html', 'subscriptions/partials/plans_content.html')
def plans(request):
    """Plans view."""
    hub_id = request.session.get('hub_id')
    return {}


@login_required
@with_module_nav('subscriptions', 'subscriptions')
@htmx_view('subscriptions/pages/subscriptions.html', 'subscriptions/partials/subscriptions_content.html')
def subscriptions(request):
    """Subscriptions view."""
    hub_id = request.session.get('hub_id')
    return {}


@login_required
@with_module_nav('subscriptions', 'settings')
@htmx_view('subscriptions/pages/settings.html', 'subscriptions/partials/settings_content.html')
def settings(request):
    """Settings view."""
    hub_id = request.session.get('hub_id')
    return {}

