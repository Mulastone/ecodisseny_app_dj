from django.shortcuts import render
from dal import autocomplete
from .models import Poblacio

class PoblacioAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Poblacio.objects.all()

        parroquia_id = self.forwarded.get('parroquia', None)
        if parroquia_id:
            qs = qs.filter(id_parroquia=parroquia_id)

        if self.q:
            qs = qs.filter(poblacio__icontains=self.q)

        return qs
