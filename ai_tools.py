"""AI tools for the Subscriptions module."""
from assistant.tools import AssistantTool, register_tool


@register_tool
class ListSubscriptions(AssistantTool):
    name = "list_subscriptions"
    description = "List subscriptions with optional status filter."
    module_id = "subscriptions"
    required_permission = "subscriptions.view_subscription"
    parameters = {
        "type": "object",
        "properties": {
            "status": {"type": "string", "description": "Filter: active, paused, cancelled, expired"},
            "limit": {"type": "integer", "description": "Max results (default 20)"},
        },
        "required": [],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from subscriptions.models import Subscription
        qs = Subscription.objects.select_related('plan').order_by('-start_date')
        if args.get('status'):
            qs = qs.filter(status=args['status'])
        limit = args.get('limit', 20)
        return {
            "subscriptions": [
                {
                    "id": str(s.id),
                    "plan": s.plan.name if s.plan else None,
                    "customer_name": s.customer_name,
                    "customer_email": s.customer_email,
                    "status": s.status,
                    "start_date": str(s.start_date) if s.start_date else None,
                    "next_billing": str(s.next_billing) if s.next_billing else None,
                    "auto_renew": s.auto_renew,
                }
                for s in qs[:limit]
            ],
            "total": qs.count(),
        }


@register_tool
class ListPlans(AssistantTool):
    name = "list_subscription_plans"
    description = "List available subscription plans."
    module_id = "subscriptions"
    required_permission = "subscriptions.view_subscription"
    parameters = {
        "type": "object",
        "properties": {},
        "required": [],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from subscriptions.models import Plan
        plans = Plan.objects.filter(is_active=True).order_by('price')
        return {
            "plans": [
                {
                    "id": str(p.id),
                    "name": p.name,
                    "price": str(p.price),
                    "billing_period": p.billing_period,
                    "description": p.description,
                }
                for p in plans
            ]
        }


@register_tool
class CreateSubscription(AssistantTool):
    name = "create_subscription"
    description = "Create a new subscription for a customer."
    module_id = "subscriptions"
    required_permission = "subscriptions.change_subscription"
    requires_confirmation = True
    parameters = {
        "type": "object",
        "properties": {
            "plan_id": {"type": "string", "description": "Plan ID"},
            "customer_name": {"type": "string", "description": "Customer name"},
            "customer_email": {"type": "string", "description": "Customer email"},
            "start_date": {"type": "string", "description": "Start date (YYYY-MM-DD)"},
            "auto_renew": {"type": "boolean", "description": "Auto-renew (default true)"},
        },
        "required": ["plan_id", "customer_name", "start_date"],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from subscriptions.models import Subscription
        s = Subscription.objects.create(
            plan_id=args['plan_id'],
            customer_name=args['customer_name'],
            customer_email=args.get('customer_email', ''),
            start_date=args['start_date'],
            auto_renew=args.get('auto_renew', True),
            status='active',
        )
        return {"id": str(s.id), "customer_name": s.customer_name, "plan": s.plan.name, "created": True}


@register_tool
class UpdateSubscriptionStatus(AssistantTool):
    name = "update_subscription_status"
    description = "Pause, resume, or cancel a subscription."
    module_id = "subscriptions"
    required_permission = "subscriptions.change_subscription"
    requires_confirmation = True
    parameters = {
        "type": "object",
        "properties": {
            "subscription_id": {"type": "string", "description": "Subscription ID"},
            "action": {"type": "string", "description": "Action: pause, resume, cancel"},
        },
        "required": ["subscription_id", "action"],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from subscriptions.models import Subscription
        s = Subscription.objects.get(id=args['subscription_id'])
        action = args['action']
        if action == 'pause' and s.status == 'active':
            s.status = 'paused'
        elif action == 'resume' and s.status == 'paused':
            s.status = 'active'
        elif action == 'cancel':
            s.status = 'cancelled'
        else:
            return {"error": f"Cannot {action} a {s.status} subscription"}
        s.save(update_fields=['status'])
        return {"id": str(s.id), "customer_name": s.customer_name, "status": s.status}
