from django.contrib import admin, messages
from django.db import IntegrityError
from django.core.exceptions import ValidationError

def safe_delete_selected(modeladmin, request, queryset):
    eliminats = []
    errors = []

    for obj in queryset:
        try:
            obj.delete()
            eliminats.append(str(obj))
        except (IntegrityError, ValidationError):
            errors.append(str(obj))

    # Mensajes personalizados
    model_label = getattr(modeladmin, 'delete_model_label', 'element')
    plural_model_label = getattr(modeladmin, 'delete_model_label_plural', model_label + 's')

    if eliminats:
        modeladmin.message_user(
            request,
            f"S'han eliminat correctament {len(eliminats)} {plural_model_label}: {', '.join(eliminats)}.",
            level=messages.SUCCESS
        )
    if errors:
        for name in errors:
            modeladmin.message_user(
                request,
                f"No es pot eliminar '{name}' perquè està en ús.",
                level=messages.ERROR
            )

class SafeDeleteAdmin(admin.ModelAdmin):
    actions = [safe_delete_selected]

    def get_actions(self, request):
        actions = super().get_actions(request)
        actions.pop('delete_selected', None)  # elimina la acción por defecto
        return actions
