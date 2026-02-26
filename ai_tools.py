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
