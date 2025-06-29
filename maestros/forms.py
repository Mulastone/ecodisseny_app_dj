from dal import autocomplete
from dal_select2.widgets import ModelSelect2
from django import forms
from .models import Clients

class ClientAdminForm(forms.ModelForm):
    class Meta:
        model = Clients
        fields = '__all__'
        widgets = {
            'poblacio': ModelSelect2(
                url='poblacio-autocomplete',
                forward=['parroquia']
            )
        }
