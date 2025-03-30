from django.contrib import admin, messages
from .forms import ClientAdminForm
from django.contrib.admin import SimpleListFilter
from .models import Clients, Parroquia, Poblacio, Recurso, Tipusrecurso, Tasca, Treballs, Ubicacio, TasquesTreball, Desplacaments, Hores, DepartamentClient, PersonaContactClient
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.urls import reverse
from .admin_utils import SafeDeleteAdmin, safe_delete_selected

@admin.register(Clients)
class ClientsAdmin(admin.ModelAdmin):
    form = ClientAdminForm
    list_display = ("nomclient", "mail", "telefon", "nrt")
    search_fields = ("nomclient", "mail", "nrt")
    verbose_name = "Client"
    verbose_name_plural = "Clients"
    fieldsets = (
        ("Informació general", {
            'fields': ('nomclient', 'rsocial', 'nrt', 'telefon', 'mail')
        }),
        ("Adreça", {
            'fields': ('parroquia', 'poblacio', 'carrer', 'nro', 'escala', 'pis', 'porta'),
            'classes': ('collapse',),  # opcional: hace que este bloque se pueda plegar
        }),
        
        )

@admin.register(Parroquia)
class ParroquiaAdmin(admin.ModelAdmin):
    list_display = ("parroquia",)
    search_fields = ("parroquia",)

# Filtro personalizado para Parroquia
class ParroquiaFilter(SimpleListFilter):
    title = 'Parròquia'
    parameter_name = 'id_parroquia'

    def lookups(self, request, model_admin):
        from .models import Parroquia
        return [(p.id_parroquia, p.parroquia) for p in Parroquia.objects.all()]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(id_parroquia__id_parroquia=self.value())
        return queryset

# Admin de Poblacio
@admin.register(Poblacio)
class PoblacioAdmin(admin.ModelAdmin):
    list_display = ("poblacio", "codipostal", "mostrar_parroquia")
    list_filter = (ParroquiaFilter,)
    list_per_page = 8
    search_fields = ("poblacio",)
    verbose_name = "Població"
    verbose_name_plural = "Poblacions"

    @admin.display(description="Parròquia", ordering="id_parroquia__parroquia")
    def mostrar_parroquia(self, obj):
        return obj.id_parroquia.parroquia if obj.id_parroquia else "-"


@admin.register(Tipusrecurso)
class TipusrecursoAdmin(admin.ModelAdmin):
    list_display = ("tipus",)

# Filtro personalizado para Tipusrecurso
class TipusRecursoFilter(admin.SimpleListFilter):
    title = 'Tipus de Recurs'
    parameter_name = 'tipusrecurso'

    def lookups(self, request, model_admin):
        return [(tipus.id_tipusrecurso, tipus.tipus) for tipus in Tipusrecurso.objects.all()]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(id_tipusrecurso=self.value())
        return queryset

# Admin personalizado
@admin.register(Recurso)
class RecursoAdmin(admin.ModelAdmin):
    list_display = ("name", "mostrar_tipus", "preutancat", "preuhora")
    list_filter = (TipusRecursoFilter, "preutancat")
    search_fields = ("name",)

    def mostrar_tipus(self, obj):
        return obj.id_tipusrecurso.tipus if obj.id_tipusrecurso else "-"
    mostrar_tipus.short_description = "Tipus"
    mostrar_tipus.admin_order_field = "id_tipusrecurso__tipus"
    

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


# Filtros personalizados
class TascaFilter(SimpleListFilter):
    title = 'Tasca'
    parameter_name = 'id_tasca'

    def lookups(self, request, model_admin):
        return [(t.id_tasca, t.tasca) for t in Tasca.objects.all()]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(id_tasca__id_tasca=self.value())
        return queryset

class TreballFilter(SimpleListFilter):
    title = 'Treball'
    parameter_name = 'id_treball'

    def lookups(self, request, model_admin):
        return [(t.id_treball, t.descripcio) for t in Treballs.objects.all()]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(id_treball__id_treball=self.value())
        return queryset

# Admin personalizado
@admin.register(TasquesTreball)
class TasquesTreballAdmin(admin.ModelAdmin):
    list_display = ("mostrar_tasca", "mostrar_treball", "observacions")
    list_filter = (TascaFilter, TreballFilter)
    search_fields = ("id_tasca__tasca", "id_treball__descripcio")

    @admin.display(description="Tasca", ordering="id_tasca__tasca")
    def mostrar_tasca(self, obj):
        return obj.id_tasca.tasca if obj.id_tasca else "-"

    @admin.display(description="Treball", ordering="id_treball__descripcio")
    def mostrar_treball(self, obj):
        return obj.id_treball.descripcio if obj.id_treball else "-"


 #Filtro personalizado para Parròquia
class ParroquiaFilter(SimpleListFilter):
    title = 'Parròquia'
    parameter_name = 'id_parroquia'

    def lookups(self, request, model_admin):
        return [(p.id_parroquia, p.parroquia) for p in Parroquia.objects.all()]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(id_parroquia__id_parroquia=self.value())
        return queryset

# Filtro personalizado para Ubicació
class UbicacioFilter(SimpleListFilter):
    title = 'Ubicació'
    parameter_name = 'id_ubicacio'

    def lookups(self, request, model_admin):
        return [(u.id_ubicacio, u.ubicacio) for u in Ubicacio.objects.all()]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(id_ubicacio__id_ubicacio=self.value())
        return queryset

# Admin personalizado para Desplacaments
@admin.register(Desplacaments)
class DesplacamentsAdmin(admin.ModelAdmin):
    list_display = ("mostrar_parroquia", "mostrar_ubicacio", "mostrar_tasca", "increment_hores")
    list_filter = (ParroquiaFilter, UbicacioFilter, TascaFilter)
    search_fields = ("id_parroquia__parroquia", "id_ubicacio__ubicacio", "id_tasca__tasca")
    list_per_page = 10
    ordering = ["-datacreacio"]

    @admin.display(description="Parròquia", ordering="id_parroquia__parroquia")
    def mostrar_parroquia(self, obj):
        return obj.id_parroquia.parroquia if obj.id_parroquia else "-"

    @admin.display(description="Ubicació", ordering="id_ubicacio__ubicacio")
    def mostrar_ubicacio(self, obj):
        return obj.id_ubicacio.ubicacio if obj.id_ubicacio else "-"

    @admin.display(description="Tasca", ordering="id_tasca__tasca")
    def mostrar_tasca(self, obj):
        return obj.id_tasca.tasca if obj.id_tasca else "-"
    

@admin.register(Hores)
class HoresAdmin(admin.ModelAdmin):
    list_display = ("hores",)
    search_fields = ("hores",)
    verbose_name = "Hora"
    verbose_name_plural = "Hores"
    ordering = ["hores"]
    list_per_page = 10

@admin.register(DepartamentClient)
class DepartamentClientAdmin(admin.ModelAdmin):
    list_display = ("nom",)
    search_fields = ("nom",)
    verbose_name = "Departament"
    verbose_name_plural = "Departaments"
    ordering = ["nom"]
    list_per_page = 10
    list_filter = ("nom",)
    search_fields = ("nom",)


# Filtro personalizado para Client
class ClientFilter(SimpleListFilter):
    title = 'Client'
    parameter_name = 'id_client'

    def lookups(self, request, model_admin):
        from .models import Clients
        return [(c.id_client, c.nomclient) for c in Clients.objects.all()]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(id_client=self.value())
        return queryset

# Admin de PersonaContactClient
@admin.register(PersonaContactClient)
class PersonaContactClientAdmin(SafeDeleteAdmin):  # 🔁 hereda de SafeDeleteAdmin
    list_display = ("nom_contacte", "mostrar_client", "telefon")  
    list_filter = (ClientFilter,)
    list_per_page = 8
    search_fields = ("nom_contacte",)

    # 🔤 Etiquetas personalizadas (opcional)
    delete_model_label = "contacte"
    delete_model_label_plural = "contactes"

    @admin.display(description="Client", ordering="id_client__nomclient")
    def mostrar_client(self, obj):
        return obj.id_client.nomclient if obj.id_client else "-"