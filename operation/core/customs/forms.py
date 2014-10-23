from django import forms
from operation.core.customs.permissions import check_view_readonly_action
from django.forms.widgets import Widget


class PermissionReadonlyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PermissionReadonlyForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance', None)
        if instance and check_view_readonly_action(instance):
            for field_name, field in self.fields.iteritems():
                if isinstance(field.widget, Widget):
                    field.widget.attrs['readonly'] = "readonly"
