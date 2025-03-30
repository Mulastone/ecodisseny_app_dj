from django.contrib import admin
from .models import Projectes
from .forms import ProjectesForm





@admin.register(Projectes)
class ProjectesAdmin(admin.ModelAdmin):
    form = ProjectesForm
    list_display = ("nom_projecte", "mostrar_client", "tancat", "data_peticio")
    search_fields = ("nom_projecte", "id_client__nomclient", "id_persona_contact__nom_contacte")
    list_filter = ("tancat", "id_parroquia", "id_client")

    @admin.display(description="Client", ordering="id_client__nomclient")
    def mostrar_client(self, obj):
        return obj.id_client.nomclient if obj.id_client else "-"
    
    @admin.display(description="DepartamentClient", ordering="id_departament__nom")
    def mostrar_departament(self, obj):
        return obj.id_departament.nom if obj.id_departament else "-"
