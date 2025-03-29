from django.contrib import admin
from .forms import ClientAdminForm
from .models import Clients, Parroquia, Poblacio, Recurso, Tipusrecurso, Tasca, Treballs, Ubicacio

@admin.register(Clients)
class ClientsAdmin(admin.ModelAdmin):
    form = ClientAdminForm
    list_display = ("nomclient", "mail", "telefon", "nrt")
    search_fields = ("nomclient", "mail", "nrt")
    verbose_name = "Client"
    verbose_name_plural = "Clients"
    fields = [
        'nomclient',
        'rsocial',
        'nrt',
        'parroquia',
        'poblacio',
        'carrer',
        'nro',
        'escala',
        'pis',
        'porta',
        'telefon',
        'mail',
    ]


@admin.register(Parroquia)
class ParroquiaAdmin(admin.ModelAdmin):
    list_display = ("parroquia",)
    search_fields = ("parroquia",)

@admin.register(Poblacio)
class PoblacioAdmin(admin.ModelAdmin):
    list_display = ("poblacio", "codipostal", "id_parroquia")
    search_fields = ("poblacio",)
    verbose_name = "Població"
    verbose_name_plural = "Poblacions"

@admin.register(Tipusrecurso)
class TipusrecursoAdmin(admin.ModelAdmin):
    list_display = ("tipus",)

@admin.register(Recurso)
class RecursoAdmin(admin.ModelAdmin):
    list_display = ("name", "preutancat", "preuhora")
    search_fields = ("name",)

@admin.register(Treballs)
class TreballsAdmin(admin.ModelAdmin):
    list_display = ("descripcio",)
    search_fields = ("descripcio",)


@admin.register(Tasca)
class TascaAdmin(admin.ModelAdmin):
    list_display = ("tasca",)
    search_fields = ("tasca",)


@admin.register(Ubicacio)
class UbicacioAdmin(admin.ModelAdmin):
    list_display = ("ubicacio",)
    search_fields = ("ubicacio",)

