"""
AI context for the Subscriptions module.
Loaded into the assistant system prompt when this module's tools are active.
"""

CONTEXT = """
## Module Knowledge: Subscriptions

### Models

**Plan** — A subscription plan template.
- `name` (CharField)
- `price` (Decimal)
- `billing_period`: 'weekly' | 'monthly' | 'quarterly' | 'yearly'
- `description`
- `is_active`

**Subscription** — A customer's active subscription to a plan.
- `plan` FK → Plan
- `customer_name`, `customer_email`: Customer info stored as plain strings (no FK to customers module)
- `status`: 'active' | 'paused' | 'cancelled' | 'expired'
- `start_date` (DateField, required)
- `end_date` (DateField, optional): When subscription ends
- `next_billing` (DateField, optional): Next billing date
- `auto_renew` (bool, default True)

### Key Flows

1. **Create subscription**: Choose a Plan → create Subscription with customer info, start_date, and initial next_billing date matching the plan's billing_period
2. **Renew**: On next_billing date, process payment → update next_billing forward by billing_period; if auto_renew=False and end_date reached, set status='expired'
3. **Pause**: Set status='paused' (billing suspended)
4. **Cancel**: Set status='cancelled'
5. **Resume**: Set status='active', recalculate next_billing

### Notes
- This is a lightweight subscription tracker. It does not handle payment processing directly.
- Customer is stored as name/email strings — no FK to the customers module.
- For recurring invoicing/billing logic, see the invoicing or contracts modules.
"""
