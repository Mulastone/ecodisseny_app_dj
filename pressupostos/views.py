from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from maestros.models import Desplacaments, Recurso, TasquesTreball, Tasca

def get_increment_hores(request):
    parroquia_id = request.GET.get('parroquia_id')
    ubicacio_id = request.GET.get('ubicacio_id')
    tasca_id = request.GET.get('tasca_id')

    if parroquia_id and ubicacio_id and tasca_id:
        desplaçament = Desplacaments.objects.filter(
            id_parroquia=parroquia_id,
            id_ubicacio=ubicacio_id,
            id_tasca=tasca_id
        ).first()

        increment = desplaçament.increment_hores if desplaçament else 0
        return JsonResponse({'increment_hores': float(increment)})
    
    return JsonResponse({'increment_hores': 0})


def get_dades_recurs(request):
    recurso_id = request.GET.get('recurso_id')
    if recurso_id:
        try:
            recurs = Recurso.objects.get(pk=recurso_id)
            return JsonResponse({
                'preu_tancat': recurs.preutancat,
                'preu_hora': float(recurs.preuhora)
            })
        except Recurso.DoesNotExist:
            pass
    return JsonResponse({'preu_tancat': 0, 'preu_hora': 0})

from django.http import JsonResponse
from django.views.decorators.http import require_GET
from maestros.models import TasquesTreball, Tasca

@require_GET
def get_tasques_treball(request):
    treball_id = request.GET.get("treball_id")
    tasques = []

    if treball_id:
        relacions = TasquesTreball.objects.filter(id_treball_id=treball_id)
        for rel in relacions:
            tasques.append({
                'id': rel.id_tasca.id_tasca,
                'tasca': rel.id_tasca.tasca,
            })

    return JsonResponse({'tasques': tasques})
