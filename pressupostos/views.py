from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.db import transaction
from datetime import datetime
from django.utils.timezone import now
from .forms import (
    PressupostForm,
    PressupostLineaFormSetCreate,
    PressupostLineaFormSetEdit
)
from .models import Pressupostos, PressupostosLineas, PressupostPDFVersion
from maestros.models import Tasca, Recurso, Desplacaments, Treballs
from projectes.models import Projectes

from django.template.loader import get_template
from weasyprint import HTML
import tempfile
from django.urls import reverse
from weasyprint import HTML
from django.core.files import File


import tempfile
from django.http import HttpResponseRedirect
from django.urls import reverse

# --- GENERAR PDF Y GUARDAR ---
def generar_pdf_y_guardar(request, pressupost_id):
    pressupost = Pressupostos.objects.get(pk=pressupost_id)
    lineas = PressupostosLineas.objects.filter(id_pressupost=pressupost)
    total = sum([l.total_linea or 0 for l in lineas])

    # Obtener el número de versión
    ultima_version = PressupostPDFVersion.objects.filter(pressupost=pressupost).first()
    nueva_version = ultima_version.version + 1 if ultima_version else 1

    # Renderizar plantilla
    template = get_template("pressupostos/pdf.html")
    html_string = template.render({
        "pressupost": pressupost,
        "lineas": lineas,
        "total_pressupost": total,
        "logo_url": request.build_absolute_uri("/static/logo_ecodisseny_positiu.png"),
        "now": now(),
        "generat_per": request.user.get_full_name() or request.user.username
    })

    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as output:
        HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(output.name)
        output.seek(0)

        # Guardar en modelo
        nueva_pdf = PressupostPDFVersion(
            pressupost=pressupost,
            version=nueva_version,
            generado_por=request.user
        )
        nueva_pdf.archivo.save(f"pressupost_{pressupost.id}_v{nueva_version}.pdf", File(output))

    return HttpResponseRedirect(reverse("pressupostos:detalle", args=[pressupost_id]))


# --- PDF VIEW ---
def ver_pdf_pressupost(request, id):
    pressupost = get_object_or_404(Pressupostos, pk=id)
    lineas = PressupostosLineas.objects.filter(id_pressupost=pressupost)
    total = sum([l.total_linea or 0 for l in lineas])

    template = get_template("pressupostos/pdf.html")
    html_string = template.render({
        "pressupost": pressupost,
        "lineas": lineas,
        "total_pressupost": total,
        "logo_url": request.build_absolute_uri("/static/logo_ecodisseny_positiu.png"),
        "now": now(),
        "generat_per": request.user.get_full_name() or request.user.username
    })

    response = HttpResponse(content_type="application/pdf")
    filename = f'pressupost_{pressupost.pk}.pdf'
    response["Content-Disposition"] = f'inline; filename="{filename}"'

    with tempfile.NamedTemporaryFile(delete=True, suffix=".pdf") as output:
        HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(output.name)
        output.seek(0)
        response.write(output.read())

    return response


# --- LISTADO DE PRESSUPOSTOS ---
def list_pressuposts(request):
    pressupostos = Pressupostos.objects.all()
    return render(request, 'pressupostos/list.html', {'pressupostos': pressupostos})

# --- FORMULARIO CREACIÓN/EDICIÓN ---
def form_pressupost(request, id=None):
    pressupost = get_object_or_404(Pressupostos, pk=id) if id else None

    if request.method == 'POST':
        form = PressupostForm(request.POST, instance=pressupost)
        formset_class = PressupostLineaFormSetEdit if pressupost else PressupostLineaFormSetCreate
        formset = formset_class(request.POST, instance=pressupost or Pressupostos())

        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    pressupost = form.save(commit=False)
                    pressupost.datamodificacio = datetime.now()
                    pressupost.save()
                    formset.instance = pressupost
                    formset.save()
                messages.success(request, 'Pressupost guardat correctament.')
                return redirect('pressupostos:list')
            except Exception as e:
                messages.error(request, f'Error al guardar: {str(e)}')
        else:
            messages.error(request, 'Formulari invàlid.')
    else:
        form = PressupostForm(instance=pressupost)
        if pressupost and pressupost.pk:
            formset = PressupostLineaFormSetEdit(instance=pressupost)
        else:
            nova_instance = Pressupostos()
            formset = PressupostLineaFormSetCreate(instance=nova_instance)

    return render(request, 'pressupostos/form.html', {
        'form': form,
        'pressupost': pressupost,
        'formset': formset
    })

# --- ELIMINAR PRESSUPOST ---
@require_http_methods(["POST"])
def delete_pressupost(request, id):
    pressupost = get_object_or_404(Pressupostos, pk=id)
    pressupost.delete()
    messages.success(request, 'Pressupost eliminat correctament.')
    return redirect('pressupostos:list')

# --- ENDPOINTS AJAX ---

def get_increment_hores(request):
    id_parroquia = request.GET.get("id_parroquia")
    id_ubicacio = request.GET.get("id_ubicacio")
    id_tasca = request.GET.get("id_tasca")

    if not (id_parroquia and id_ubicacio and id_tasca):
        return JsonResponse({"error": "Falten paràmetres"}, status=400)

    try:
        desplacament = Desplacaments.objects.filter(
            id_parroquia=id_parroquia,
            id_ubicacio=id_ubicacio,
            id_tasca=id_tasca
        ).first()

        increment = desplacament.increment_hores if desplacament else 0
        return JsonResponse({"increment_hores": float(increment)})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def get_projectes_by_client(request, id_client):
    projectes = Projectes.objects.filter(id_client=id_client, tancat=False)
    data = [{'id': p.id_projecte, 'nom': p.nom_projecte} for p in projectes]
    return JsonResponse(data, safe=False)

def get_tasques_by_treball(request, id_treball):
    try:
        treball = Treballs.objects.get(id_treball=id_treball)
        tasques = treball.tasques.all()
        tasques_data = [
            {'id': tasca.id_tasca, 'tasca': tasca.tasca}
            for tasca in tasques
        ]
        return JsonResponse({'tasques': tasques_data})
    except Treballs.DoesNotExist:
        return JsonResponse({'error': 'Treball no trobat'}, status=404)

def get_recurso_by_id(request, id_recurso):
    recurso = Recurso.objects.filter(pk=id_recurso).exclude(id_recurso=1).first()
    if recurso:
        return JsonResponse({
            "PreuTancat": recurso.preutancat,
            "PreuHora": recurso.preuhora if not recurso.preutancat else None
        })
    return JsonResponse({"error": "Recurso no trobat"}, status=404)

def veure_pressupost(request, id):
    pressupost = get_object_or_404(Pressupostos, pk=id)
    lineas = pressupost.lineas.all()
    total = sum([l.total_linea or 0 for l in lineas])

    return render(request, "pressupostos/detail.html", {
        "pressupost": pressupost,
        "lineas": lineas,
        "total": total,
    })
