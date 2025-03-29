# maestros/urls.py
from django.urls import path
from .views_autocomplete import PoblacioAutocomplete

urlpatterns = [
    path('poblacio-autocomplete/', PoblacioAutocomplete.as_view(), name='poblacio-autocomplete'),
]
