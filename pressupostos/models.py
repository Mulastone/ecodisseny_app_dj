from django.db import models
from django.utils import timezone

# Importar modelos desde maestros
from maestros.models import (
    Clients, Treballs, Tasca, Recurso, Hores,
    Parroquia, Ubicacio
)

# Importar modelos desde projectes
from projectes.models import (
    Projectes
)

class Pressupostos(models.Model):
    id_pressupost = models.AutoField(primary_key=True)
    id_client = models.ForeignKey(Clients, models.DO_NOTHING, db_column='id_client',blank=False, null=False) #buscar clients en app maestros, se filtran los proyectos en base al cliente seleccionado.
    id_projecte = models.ForeignKey(Projectes, models.DO_NOTHING, db_column='id_projecte', blank=False, null=False) #buscar projectes en app projectes
    id_parroquia = models.ForeignKey(Parroquia, models.DO_NOTHING, db_column='id_parroquia', blank=False, null=False) #buscar parroquies en app maestros
    id_ubicacio = models.ForeignKey(Ubicacio, models.DO_NOTHING, db_column='id_ubicacio', blank=False, null=False) #buscar ubicacions en app maestros
    nom_pressupost = models.CharField(max_length=255, blank=True, null=True)
    data_pressupost = models.DateField(default=timezone.now,blank=False, null=False)
    observacions = models.CharField(max_length=600, blank=True, null=True)
    tancat = models.BooleanField(default=False)
    datacreacio = models.DateTimeField(db_column='data_creacio', auto_now_add=True)
    datamodificacio = models.DateTimeField(db_column='data_modificacio', auto_now=True)


    class Meta:
        managed = False
        db_table = 'pressupostos'
        verbose_name = "Pressupost"
        verbose_name_plural = "Presuspostos"
        app_label = 'pressupostos'

    def __str__(self):
        return f"{self.nom_pressupost} ({self.id_projecte})"


class PressupostosLineas(models.Model):
    id_pressupost_linea = models.AutoField(primary_key=True)
    id_pressupost = models.ForeignKey(Pressupostos, models.DO_NOTHING, db_column='id_pressupost') # relacionar con el id_pressupost del formulario pressupostos
    id_treball = models.ForeignKey(Treballs, models.DO_NOTHING, db_column='id_treball') # buscar treballs en app maestros
    id_tasca = models.ForeignKey(Tasca, models.DO_NOTHING, db_column='id_tasca') # buscar tasques en app maestros
    quantitat = models.IntegerField() #aqui se tiene que poder poner la cantidad que se desee
    id_recurso = models.ForeignKey(Recurso, models.DO_NOTHING, db_column='id_recurso') # buscar recursos en app maestros
    preu_tancat = models.BooleanField(blank=True, null=True) # buscar en el modelo recursos e informar el preu tancat (boolean) campo solo lectura
    cost_tancat = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True) #si preu tancat es 1, se tiene que habilitar este campo para poner el coste. si preu tancat es 0, este campo no se puede modificar y por defecto se pone a 0
    id_hora = models.ForeignKey(Hores, models.DO_NOTHING, db_column='id_hora', blank=True, null=True) # buscar hores en app maestros
    increment_hores = models.DecimalField(max_digits=5, decimal_places=2) 
    """campo increment_hores = en base al idparroquia e id_ubicacio seleccionadoes en el formulario pressupostos, y al id_tasca seleccionado en este formulario y id_hora seleccionado en este formulario, 
    se tiene buscar el campo increment d'hores en deplacaments en la app maestros y traerlo es un campo de solo lectura, si el preu_tancat es 1 hay que poner 0"""
    hores_totales = models.DecimalField(max_digits=5, decimal_places=2) # aplica para preu_tancat = 0 y el cáclulo a realizar es (hores + increment_hores) * quantitat. si preu tancat es 1, este campo no se puede modificar y por defecto se pone a 0
    cost_hores = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True) # en base al reucrso seleccionado informar el campo preu_hora del model recurso de la app maestros. si preu_tancat es 1, este campo no se puede modificar y por defecto se pone a 0
    cost_hores_totals = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True) # multiplicar hores_totales * cost_hores, si prue_tancat es 1, este campo no se puede modificar y por defecto se pone a 0
    subtotal_linea = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True) # subtotal_linea = cost_hores_totals + cost_tancat.
    benefici_linea = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True) # el usuario expresa en porcentaje el incremento que se le ha de aplicar al subtotal_linea.
    total_linea = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True) # total_linea = subtotal_linea + benefici_linea (se incrementa el subotal_linea con el porcentaje que ha introducido el usuario en el campo benefici_linea)
    datacreacio = models.DateTimeField(db_column='data_creacio', auto_now_add=True)
    datamodificacio = models.DateTimeField(db_column='data_modificacio', auto_now=True)


    class Meta:
        managed = False
        db_table = 'pressupostos_lineas'
        verbose_name = "Pressuost Linea"
        verbose_name_plural = "Pessupostos Linees"
        app_label = 'pressupostos'

    def __str__(self):
        return f"L\u00ednea {self.id_pressupost_linea} - Pressupost {self.id_pressupost_id}"
    

from django.contrib.auth.models import User

class PressupostPDFVersion(models.Model):
    pressupost = models.ForeignKey("Pressupostos", on_delete=models.CASCADE, related_name="pdf_versions")
    version = models.PositiveIntegerField()
    archivo = models.FileField(upload_to="pdfs_pressupostos/")
    generado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    fecha_generado = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('pressupost', 'version')
        ordering = ['-version']

    def __str__(self):
        return f"Pressupost #{self.pressupost.id} - Versió {self.version}"
