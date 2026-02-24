"""Tests for subscriptions views."""
import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestDashboard:
    """Dashboard view tests."""

    def test_dashboard_loads(self, auth_client):
        """Test dashboard page loads."""
        url = reverse('subscriptions:dashboard')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_dashboard_htmx(self, auth_client):
        """Test dashboard HTMX partial."""
        url = reverse('subscriptions:dashboard')
        response = auth_client.get(url, HTTP_HX_REQUEST='true')
        assert response.status_code == 200

    def test_dashboard_requires_auth(self, client):
        """Test dashboard requires authentication."""
        url = reverse('subscriptions:dashboard')
        response = client.get(url)
        assert response.status_code == 302


@pytest.mark.django_db
class TestPlanViews:
    """Plan view tests."""

    def test_list_loads(self, auth_client):
        """Test list view loads."""
        url = reverse('subscriptions:plans_list')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_list_htmx(self, auth_client):
        """Test list HTMX partial."""
        url = reverse('subscriptions:plans_list')
        response = auth_client.get(url, HTTP_HX_REQUEST='true')
        assert response.status_code == 200

    def test_list_search(self, auth_client):
        """Test list search."""
        url = reverse('subscriptions:plans_list')
        response = auth_client.get(url, {'q': 'test'})
        assert response.status_code == 200

    def test_list_sort(self, auth_client):
        """Test list sorting."""
        url = reverse('subscriptions:plans_list')
        response = auth_client.get(url, {'sort': 'created_at', 'dir': 'desc'})
        assert response.status_code == 200

    def test_export_csv(self, auth_client):
        """Test CSV export."""
        url = reverse('subscriptions:plans_list')
        response = auth_client.get(url, {'export': 'csv'})
        assert response.status_code == 200
        assert 'text/csv' in response['Content-Type']

    def test_export_excel(self, auth_client):
        """Test Excel export."""
        url = reverse('subscriptions:plans_list')
        response = auth_client.get(url, {'export': 'excel'})
        assert response.status_code == 200

    def test_add_form_loads(self, auth_client):
        """Test add form loads."""
        url = reverse('subscriptions:plan_add')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_add_post(self, auth_client):
        """Test creating via POST."""
        url = reverse('subscriptions:plan_add')
        data = {
            'name': 'New Name',
            'price': '100.00',
            'billing_period': 'New Billing Period',
            'description': 'Test description',
            'is_active': 'on',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_edit_form_loads(self, auth_client, plan):
        """Test edit form loads."""
        url = reverse('subscriptions:plan_edit', args=[plan.pk])
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_edit_post(self, auth_client, plan):
        """Test editing via POST."""
        url = reverse('subscriptions:plan_edit', args=[plan.pk])
        data = {
            'name': 'Updated Name',
            'price': '100.00',
            'billing_period': 'Updated Billing Period',
            'description': 'Test description',
            'is_active': '',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_delete(self, auth_client, plan):
        """Test soft delete via POST."""
        url = reverse('subscriptions:plan_delete', args=[plan.pk])
        response = auth_client.post(url)
        assert response.status_code == 200
        plan.refresh_from_db()
        assert plan.is_deleted is True

    def test_toggle_status(self, auth_client, plan):
        """Test toggle active status."""
        url = reverse('subscriptions:plan_toggle_status', args=[plan.pk])
        original = plan.is_active
        response = auth_client.post(url)
        assert response.status_code == 200
        plan.refresh_from_db()
        assert plan.is_active != original

    def test_bulk_delete(self, auth_client, plan):
        """Test bulk delete."""
        url = reverse('subscriptions:plans_bulk_action')
        response = auth_client.post(url, {'ids': str(plan.pk), 'action': 'delete'})
        assert response.status_code == 200
        plan.refresh_from_db()
        assert plan.is_deleted is True

    def test_list_requires_auth(self, client):
        """Test list requires authentication."""
        url = reverse('subscriptions:plans_list')
        response = client.get(url)
        assert response.status_code == 302


@pytest.mark.django_db
class TestSettings:
    """Settings view tests."""

    def test_settings_loads(self, auth_client):
        """Test settings page loads."""
        url = reverse('subscriptions:settings')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_settings_requires_auth(self, client):
        """Test settings requires authentication."""
        url = reverse('subscriptions:settings')
        response = client.get(url)
        assert response.status_code == 302

