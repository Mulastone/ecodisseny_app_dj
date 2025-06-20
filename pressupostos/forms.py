from django import forms
from django.forms import ModelForm, inlineformset_factory, BaseInlineFormSet
from .models import Pressupostos, PressupostosLineas
from django.core.exceptions import ValidationError

class PressupostLineaForm(ModelForm):
    class Meta:
        model = PressupostosLineas
        exclude = ('datacreacio', 'datamodificacio')
        widgets = {
            'id_pressupost_linea': forms.HiddenInput(),  # 🔴 Añadir esto explícitamente
            'preu_tancat': forms.CheckboxInput(),
            'hores_totales': forms.NumberInput(attrs={'readonly': 'readonly'}),
            'cost_hores': forms.NumberInput(attrs={'readonly': 'readonly'}),
            'cost_hores_totals': forms.NumberInput(attrs={'readonly': 'readonly'}),
            'subtotal_linea': forms.NumberInput(attrs={'readonly': 'readonly'}),
            'total_linea': forms.NumberInput(attrs={'readonly': 'readonly'}),
            'benefici_linea': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),  # Editable como porcentaje
        }

    def clean(self):
        cleaned_data = super().clean()
        preu_tancat = cleaned_data.get("preu_tancat")
        id_hora = cleaned_data.get("id_hora")
        increment_hores = cleaned_data.get("increment_hores")
        hores_totales = cleaned_data.get("hores_totales")
        quantitat = cleaned_data.get("quantitat")
        cost_hores = cleaned_data.get("cost_hores")

        if quantitat is not None and quantitat < 0:
            self.add_error("quantitat", "La quantitat no pot ser negativa.")

        if not preu_tancat and cost_hores is not None and cost_hores < 0:
            self.add_error("cost_hores", "El cost per hora no pot ser negatiu.")

        if preu_tancat:
            if increment_hores not in (None, 0):
                self.add_error("increment_hores", "Ha de ser 0 si Preu Tancat està activat.")
            if hores_totales not in (None, 0):
                self.add_error("hores_totales", "Ha de ser 0 si Preu Tancat està activat.")
            if id_hora:
                self.add_error("id_hora", "Ha d'estar buit si Preu Tancat està activat.")
        else:
            if not id_hora:
                self.add_error("id_hora", "És obligatori si Preu Tancat no està activat.")

        id_tasca = cleaned_data.get("id_tasca")
        id_recurso = cleaned_data.get("id_recurso")
        if not id_tasca:
            self.add_error("id_tasca", "Cal seleccionar una tasca.")
        if not id_recurso:
            self.add_error("id_recurso", "Cal seleccionar un recurs.")

        return cleaned_data
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 🔴 Fuerza el campo como oculto si está presente
        if 'id_pressupost_linea' in self.fields:
            self.fields['id_pressupost_linea'].widget = forms.HiddenInput()

class BasePressupostLineaFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        has_linea = False
        for form in self.forms:
            if self.can_delete and self._should_delete_form(form):
                continue
            if not form.cleaned_data:
                continue
            if not form.cleaned_data.get("id_tasca") or not form.cleaned_data.get("id_recurso"):
                raise ValidationError("Totes les línies han de tenir una tasca i un recurs.")
            has_linea = True
        if not has_linea:
            raise ValidationError("El pressupost ha de tenir almenys una línia activa.")

# Factory para crear (extra=1)
PressupostLineaFormSetCreate = inlineformset_factory(
    Pressupostos,
    PressupostosLineas,
    form=PressupostLineaForm,
    formset=BasePressupostLineaFormSet,
    extra=1,
    can_delete=True
)

# Factory para editar (extra=0)
PressupostLineaFormSetEdit = inlineformset_factory(
    Pressupostos,
    PressupostosLineas,
    form=PressupostLineaForm,
    formset=BasePressupostLineaFormSet,
    extra=0,
    can_delete=True
)

class PressupostForm(ModelForm):
    class Meta:
        model = Pressupostos
        exclude = ('datacreacio', 'datamodificacio')
        widgets = {
            'data_pressupost': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['data_pressupost'].input_formats = ['%Y-%m-%d']

    def clean(self):
        cleaned_data = super().clean()
        id_client = cleaned_data.get("id_client")
        id_projecte = cleaned_data.get("id_projecte")
        if id_projecte and id_client and id_projecte.id_client != id_client:
            self.add_error("id_projecte", "El projecte no pertany al client seleccionat.")
        return cleaned_data
    


    
