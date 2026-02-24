"""Tests for subscriptions models."""
import pytest
from django.utils import timezone

from subscriptions.models import Plan


@pytest.mark.django_db
class TestPlan:
    """Plan model tests."""

    def test_create(self, plan):
        """Test Plan creation."""
        assert plan.pk is not None
        assert plan.is_deleted is False

    def test_str(self, plan):
        """Test string representation."""
        assert str(plan) is not None
        assert len(str(plan)) > 0

    def test_soft_delete(self, plan):
        """Test soft delete."""
        pk = plan.pk
        plan.is_deleted = True
        plan.deleted_at = timezone.now()
        plan.save()
        assert not Plan.objects.filter(pk=pk).exists()
        assert Plan.all_objects.filter(pk=pk).exists()

    def test_queryset_excludes_deleted(self, hub_id, plan):
        """Test default queryset excludes deleted."""
        plan.is_deleted = True
        plan.deleted_at = timezone.now()
        plan.save()
        assert Plan.objects.filter(hub_id=hub_id).count() == 0

    def test_toggle_active(self, plan):
        """Test toggling is_active."""
        original = plan.is_active
        plan.is_active = not original
        plan.save()
        plan.refresh_from_db()
        assert plan.is_active != original


