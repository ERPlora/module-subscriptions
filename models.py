from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models.base import HubBaseModel

BILLING_PERIOD = [
    ('weekly', _('Weekly')),
    ('monthly', _('Monthly')),
    ('quarterly', _('Quarterly')),
    ('yearly', _('Yearly')),
]

SUB_STATUS = [
    ('active', _('Active')),
    ('paused', _('Paused')),
    ('cancelled', _('Cancelled')),
    ('expired', _('Expired')),
]

class Plan(HubBaseModel):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    price = models.DecimalField(max_digits=10, decimal_places=2, default='0', verbose_name=_('Price'))
    billing_period = models.CharField(max_length=20, default='monthly', choices=BILLING_PERIOD, verbose_name=_('Billing Period'))
    description = models.TextField(blank=True, verbose_name=_('Description'))
    is_active = models.BooleanField(default=True, verbose_name=_('Is Active'))

    class Meta(HubBaseModel.Meta):
        db_table = 'subscriptions_plan'

    def __str__(self):
        return self.name


class Subscription(HubBaseModel):
    plan = models.ForeignKey('Plan', on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=255, verbose_name=_('Customer Name'))
    customer_email = models.EmailField(blank=True, verbose_name=_('Customer Email'))
    status = models.CharField(max_length=20, default='active', choices=SUB_STATUS, verbose_name=_('Status'))
    start_date = models.DateField(verbose_name=_('Start Date'))
    end_date = models.DateField(null=True, blank=True, verbose_name=_('End Date'))
    next_billing = models.DateField(null=True, blank=True, verbose_name=_('Next Billing'))
    auto_renew = models.BooleanField(default=True, verbose_name=_('Auto Renew'))

    class Meta(HubBaseModel.Meta):
        db_table = 'subscriptions_subscription'

    def __str__(self):
        return str(self.id)

