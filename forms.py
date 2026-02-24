from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Plan

class PlanForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields = ['name', 'price', 'billing_period', 'description', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'price': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'number'}),
            'billing_period': forms.Select(attrs={'class': 'select select-sm w-full'}),
            'description': forms.Textarea(attrs={'class': 'textarea textarea-sm w-full', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'toggle'}),
        }

