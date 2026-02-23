    from django.utils.translation import gettext_lazy as _

    MODULE_ID = 'subscriptions'
    MODULE_NAME = _('Subscriptions & Memberships')
    MODULE_VERSION = '1.0.0'
    MODULE_ICON = 'repeat-outline'
    MODULE_DESCRIPTION = _('Recurring billing, plans and membership management')
    MODULE_AUTHOR = 'ERPlora'
    MODULE_CATEGORY = 'finance'

    MENU = {
        'label': _('Subscriptions & Memberships'),
        'icon': 'repeat-outline',
        'order': 46,
    }

    NAVIGATION = [
        {'label': _('Dashboard'), 'icon': 'speedometer-outline', 'id': 'dashboard'},
{'label': _('Plans'), 'icon': 'layers-outline', 'id': 'plans'},
{'label': _('Subscriptions'), 'icon': 'repeat-outline', 'id': 'subscriptions'},
{'label': _('Settings'), 'icon': 'settings-outline', 'id': 'settings'},
    ]

    DEPENDENCIES = []

    PERMISSIONS = [
        'subscriptions.view_subscription',
'subscriptions.add_subscription',
'subscriptions.change_subscription',
'subscriptions.delete_subscription',
'subscriptions.view_plan',
'subscriptions.add_plan',
'subscriptions.change_plan',
'subscriptions.manage_settings',
    ]
