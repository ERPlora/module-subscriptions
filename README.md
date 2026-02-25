# Subscriptions & Memberships Module

Recurring billing, plans and membership management.

## Features

- Define subscription plans with flexible billing periods (weekly, monthly, quarterly, yearly)
- Create and manage customer subscriptions with auto-renewal support
- Track subscription status (active, paused, cancelled, expired)
- Monitor next billing dates and subscription end dates
- Dashboard with subscription metrics and plan performance

## Installation

This module is installed automatically via the ERPlora Marketplace.

## Configuration

Access settings via: **Menu > Subscriptions & Memberships > Settings**

## Usage

Access via: **Menu > Subscriptions & Memberships**

### Views

| View | URL | Description |
|------|-----|-------------|
| Dashboard | `/m/subscriptions/dashboard/` | Subscription overview and key metrics |
| Plans | `/m/subscriptions/plans/` | Create and manage subscription plans |
| Subscriptions | `/m/subscriptions/subscriptions/` | List and manage active subscriptions |
| Settings | `/m/subscriptions/settings/` | Module configuration |

## Models

| Model | Description |
|-------|-------------|
| `Plan` | Subscription plan with name, price, billing period (weekly/monthly/quarterly/yearly), description, and active status |
| `Subscription` | Customer subscription linking to a plan with customer name/email, status, start/end dates, next billing date, and auto-renew flag |

## Permissions

| Permission | Description |
|------------|-------------|
| `subscriptions.view_subscription` | View subscriptions |
| `subscriptions.add_subscription` | Create new subscriptions |
| `subscriptions.change_subscription` | Edit existing subscriptions |
| `subscriptions.delete_subscription` | Delete subscriptions |
| `subscriptions.view_plan` | View subscription plans |
| `subscriptions.add_plan` | Create new plans |
| `subscriptions.change_plan` | Edit existing plans |
| `subscriptions.manage_settings` | Manage module settings |

## License

MIT

## Author

ERPlora Team - support@erplora.com
