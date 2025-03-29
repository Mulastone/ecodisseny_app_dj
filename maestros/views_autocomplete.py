# maestros/views_autocomplete.py
from dal import autocomplete
from django import forms
from .models import Poblacio

class PoblacioAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Poblacio.objects.none()

        qs = Poblacio.objects.all()

        parroquia_id = self.forwarded.get('parroquia', None)
        if parroquia_id:
            qs = qs.filter(id_parroquia=parroquia_id)

        return qs
