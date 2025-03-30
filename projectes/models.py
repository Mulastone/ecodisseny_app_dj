from django.db import models
from django.utils import timezone

# Importar modelos desde maestros
from maestros.models import (
    Clients, DepartamentClient, PersonaContactClient,
    Parroquia, Ubicacio
)

class Projectes(models.Model):
    id_projecte = models.AutoField(primary_key=True)
    nom_projecte = models.CharField(max_length=255, blank=False, null=False)
    data_peticio = models.DateField(default=timezone.now, blank=False, null=False)
    id_client = models.ForeignKey(Clients, models.DO_NOTHING, verbose_name="Client",db_column='id_client')
    id_departament = models.ForeignKey(DepartamentClient, models.DO_NOTHING, verbose_name="Departament Client",db_column='id_departament')
    id_persona_contact = models.ForeignKey(PersonaContactClient, models.DO_NOTHING, verbose_name="Persona Contacte",db_column='id_persona_contact')
    id_parroquia = models.ForeignKey(Parroquia, models.DO_NOTHING, verbose_name="Parroquia",db_column='id_parroquia')
    id_ubicacio = models.ForeignKey(Ubicacio, models.DO_NOTHING, verbose_name="Ubicació",db_column='id_ubicacio')
    observacions = models.CharField(max_length=1200,blank=True, null=True)
    tancat = models.BooleanField(default=False)
    datacreacio = models.DateTimeField(db_column='data_creacio', auto_now_add=True)
    datamodificacio = models.DateTimeField(db_column='data_modificacio', auto_now=True)

    class Meta:
        managed = False
        db_table = 'projectes'
        verbose_name = "Projecte"
        verbose_name_plural = "Projectes"

    def __str__(self):
        return self.nom_projecte
