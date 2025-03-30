# projectes/forms.py
from dal import autocomplete
from django import forms
from .models import Projectes

class ProjectesForm(forms.ModelForm):
    class Meta:
        model = Projectes
        fields = '__all__'
        widgets = {
            'id_persona_contact': autocomplete.ModelSelect2(
                url='autocomplete_persona_contacte',
                forward=['id_client']
            )
        }
