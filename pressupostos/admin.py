

# Register your models here.

from django.contrib import admin
from .models import Pressupostos, PressupostosLineas
from maestros.models import Desplacaments


class PressupostosLineasInline(admin.TabularInline):
    model = PressupostosLineas
    extra = 1
    
    readonly_fields = [
        'preu_tancat', 'increment_hores', 'hores_totales',
        'cost_hores', 'cost_hores_totals', 'subtotal_linea'
    ]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "id_hora":
            kwargs["queryset"] = db_field.remote_field.model.objects.order_by("hores")
        if db_field.name == "id_tasca":
            kwargs["queryset"] = db_field.remote_field.model.objects.order_by("tasca")
        if db_field.name == "id_treball":
            kwargs["queryset"] = db_field.remote_field.model.objects.order_by("descripcio")
        if db_field.name == "id_recurso":
            kwargs["queryset"] = db_field.remote_field.model.objects.order_by("name")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)

        def formfield_for_dbfield(db_field, **kwargs):
            formfield = super(formset.form, formset.form).formfield_for_dbfield(db_field, **kwargs)
            if db_field.name == 'benefici_linea':
                formfield.help_text = "Escriu un percentatge (per ex. 10 per a un 10%)"
            return formfield

        formset.form.formfield_for_dbfield = formfield_for_dbfield
        return formset


@admin.register(Pressupostos)
class PressupostosAdmin(admin.ModelAdmin):
    list_display = ("nom_pressupost", "mostrar_projecte", "mostrar_client", "data_pressupost", "tancat")
    search_fields = ("nom_pressupost","id_projecte", "id_client")
    list_filter = ("id_client", "id_projecte","tancat", "data_pressupost")
    inlines = [PressupostosLineasInline]
    readonly_fields = ["pressupost_total_display"]  # <- Añadir el campo readonly
    fieldsets = (
        (None, {
            "fields": (
                "nom_pressupost",
                "id_projecte",
                "id_client",
                "id_parroquia",
                "id_ubicacio",
                "data_pressupost",
                "tancat",
                "observacions",
                "pressupost_total_display",  # <- Mostrar al final
            )
        }),
    )

    @admin.display(description="Total Pressupost")
    def pressupost_total_display(self, obj):
        if not obj.pk:
            return "Cal desar el pressupost primer."
        total = obj.pressupostoslineas_set.aggregate(models.Sum('total_linea'))['total_linea__sum']
        return f"{total:.2f} €" if total else "0.00 €"

    @admin.display(description="Projecte")
    def mostrar_projecte(self, obj):
        return obj.id_projecte.nom_projecte if obj.id_projecte else "-"

    @admin.display(description="Client")
    def mostrar_client(self, obj):
        return obj.id_client.nomclient if obj.id_client else "-"

    class Media:
        js = ('js/pressupostos_total.js',)
