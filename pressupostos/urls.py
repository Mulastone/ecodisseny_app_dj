from django.urls import path
from . import views

urlpatterns = [
    path('ajax/get_increment_hores/', views.get_increment_hores, name='get_increment_hores'),
    path('ajax/get_dades_recurs/', views.get_dades_recurs, name='get_dades_recurs'),
    path('ajax/get_tasques_treball/', views.get_tasques_treball, name='get_tasques_treball'),
]
