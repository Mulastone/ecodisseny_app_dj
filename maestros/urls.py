from django.urls import path
from dal import autocomplete
from .models import PersonaContactClient, Poblacio

class PoblacioAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Poblacio.objects.none()

        qs = Poblacio.objects.all()

        parroquia_id = self.forwarded.get('parroquia', None)
        if parroquia_id:
            qs = qs.filter(id_parroquia=parroquia_id)

        return qs

class PersonaContactAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = PersonaContactClient.objects.all()

        client_id = self.forwarded.get('id_client', None)
        if client_id:
            qs = qs.filter(id_client_id=client_id)

        if self.q:
            qs = qs.filter(nom_contacte__icontains=self.q)

        return qs

# Si vas a usar ProjectesAutocomplete, importa su clase:
# from pressupostos.views import ProjectesAutocomplete

urlpatterns = [
    path('poblacio-autocomplete/', PoblacioAutocomplete.as_view(), name='poblacio-autocomplete'),
    path('autocomplete/persona-contacte/', PersonaContactAutocomplete.as_view(), name='autocomplete_persona_contacte'),

    # Descomenta si tienes esta clase en views:
    # path('projectes-autocomplete/', ProjectesAutocomplete.as_view(), name='projectes-autocomplete'),
]
