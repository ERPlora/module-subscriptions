# Subscriptions & Memberships

## Overview

| Property | Value |
|----------|-------|
| **Module ID** | `subscriptions` |
| **Version** | `1.0.0` |
| **Icon** | `repeat-outline` |
| **Dependencies** | None |

## Models

### `Plan`

Plan(id, hub_id, created_at, updated_at, created_by, updated_by, is_deleted, deleted_at, name, price, billing_period, description, is_active)

| Field | Type | Details |
|-------|------|---------|
| `name` | CharField | max_length=255 |
| `price` | DecimalField |  |
| `billing_period` | CharField | max_length=20, choices: weekly, monthly, quarterly, yearly |
| `description` | TextField | optional |
| `is_active` | BooleanField |  |

### `Subscription`

Subscription(id, hub_id, created_at, updated_at, created_by, updated_by, is_deleted, deleted_at, plan, customer_name, customer_email, status, start_date, end_date, next_billing, auto_renew)

| Field | Type | Details |
|-------|------|---------|
| `plan` | ForeignKey | → `subscriptions.Plan`, on_delete=CASCADE |
| `customer_name` | CharField | max_length=255 |
| `customer_email` | EmailField | max_length=254, optional |
| `status` | CharField | max_length=20, choices: active, paused, cancelled, expired |
| `start_date` | DateField |  |
| `end_date` | DateField | optional |
| `next_billing` | DateField | optional |
| `auto_renew` | BooleanField |  |

## Cross-Module Relationships

| From | Field | To | on_delete | Nullable |
|------|-------|----|-----------|----------|
| `Subscription` | `plan` | `subscriptions.Plan` | CASCADE | No |

## URL Endpoints

Base path: `/m/subscriptions/`

| Path | Name | Method |
|------|------|--------|
| `(root)` | `dashboard` | GET |
| `subscriptions/` | `subscriptions` | GET |
| `plans/` | `plans_list` | GET |
| `plans/add/` | `plan_add` | GET/POST |
| `plans/<uuid:pk>/edit/` | `plan_edit` | GET |
| `plans/<uuid:pk>/delete/` | `plan_delete` | GET/POST |
| `plans/<uuid:pk>/toggle/` | `plan_toggle_status` | GET |
| `plans/bulk/` | `plans_bulk_action` | GET/POST |
| `settings/` | `settings` | GET |

## Permissions

| Permission | Description |
|------------|-------------|
| `subscriptions.view_subscription` | View Subscription |
| `subscriptions.add_subscription` | Add Subscription |
| `subscriptions.change_subscription` | Change Subscription |
| `subscriptions.delete_subscription` | Delete Subscription |
| `subscriptions.view_plan` | View Plan |
| `subscriptions.add_plan` | Add Plan |
| `subscriptions.change_plan` | Change Plan |
| `subscriptions.manage_settings` | Manage Settings |

**Role assignments:**

- **admin**: All permissions
- **manager**: `add_plan`, `add_subscription`, `change_plan`, `change_subscription`, `view_plan`, `view_subscription`
- **employee**: `add_subscription`, `view_plan`, `view_subscription`

## Navigation

| View | Icon | ID | Fullpage |
|------|------|----|----------|
| Dashboard | `speedometer-outline` | `dashboard` | No |
| Plans | `layers-outline` | `plans` | No |
| Subscriptions | `repeat-outline` | `subscriptions` | No |
| Settings | `settings-outline` | `settings` | No |

## AI Tools

Tools available for the AI assistant:

### `list_subscriptions`

List subscriptions with optional status filter.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `status` | string | No | Filter: active, paused, cancelled, expired |
| `limit` | integer | No | Max results (default 20) |

### `list_subscription_plans`

List available subscription plans.

### `create_subscription`

Create a new subscription for a customer.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `plan_id` | string | Yes | Plan ID |
| `customer_name` | string | Yes | Customer name |
| `customer_email` | string | No | Customer email |
| `start_date` | string | Yes | Start date (YYYY-MM-DD) |
| `auto_renew` | boolean | No | Auto-renew (default true) |

### `update_subscription_status`

Pause, resume, or cancel a subscription.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `subscription_id` | string | Yes | Subscription ID |
| `action` | string | Yes | Action: pause, resume, cancel |

## File Structure

```
README.md
__init__.py
admin.py
ai_tools.py
apps.py
forms.py
locale/
  en/
    LC_MESSAGES/
      django.po
  es/
    LC_MESSAGES/
      django.po
migrations/
  0001_initial.py
  __init__.py
models.py
module.py
static/
  icons/
    icon.svg
  subscriptions/
    css/
    js/
templates/
  subscriptions/
    pages/
      dashboard.html
      index.html
      plan_add.html
      plan_edit.html
      plans.html
      settings.html
      subscriptions.html
    partials/
      dashboard_content.html
      panel_plan_add.html
      panel_plan_edit.html
      plan_add_content.html
      plan_edit_content.html
      plans_content.html
      plans_list.html
      settings_content.html
      subscriptions_content.html
tests/
  __init__.py
  conftest.py
  test_models.py
  test_views.py
urls.py
views.py
```
