from django.db import models, IntegrityError
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
from django.core.exceptions import ValidationError

# Puedes extender el modelo base para capturar errores en save()
class SafeSaveModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        try:
            super().save(*args, **kwargs)
        except IntegrityError as e:
            raise ValidationError(f"Error d'integritat: {str(e)}")
        
        

        


class Clients(SafeSaveModel):
    id_client = models.AutoField(primary_key=True, verbose_name="ID")
    nomclient = models.CharField("Nom del Client", max_length=100, blank=False, null=False)
    rsocial = models.CharField("Raó Social", max_length=100, blank=True, null=True)
    nrt = models.CharField("NRT", max_length=100, blank=True, null=True)
    parroquia = models.ForeignKey('Parroquia', models.DO_NOTHING, blank=True, null=True, verbose_name="Parròquia")
    poblacio = models.ForeignKey('Poblacio', models.DO_NOTHING, blank=True, null=True, verbose_name="Població")
    carrer = models.CharField("Carrer", max_length=100, blank=True, null=True)
    nro = models.CharField("Número", max_length=50, blank=True, null=True)
    escala = models.CharField("Escala", max_length=50, blank=True, null=True)
    pis = models.IntegerField("Pis", blank=True, null=True)
    porta = models.CharField("Porta", max_length=50, blank=True, null=True)
    telefon = PhoneNumberField("Telèfon", blank=False, null=False)
    mail = models.EmailField("Correu electrònic", max_length=100, blank=True, null=True)
    datacreacio = models.DateTimeField(db_column='DataCreacio', auto_now_add=True)
    datamodificacio = models.DateTimeField(db_column='DataModificacio', auto_now=True)

    class Meta:
        managed = False
        db_table = 'clients'
        verbose_name = "Client"
        verbose_name_plural = "Clients"
        app_label = 'maestros'

    def __str__(self):
        return self.nomclient or "Client sense nom"


class Parroquia(SafeSaveModel):
    id_parroquia = models.AutoField(primary_key=True)
    parroquia = models.CharField(db_column='Parroquia', max_length=100, blank=False, null=False)
    datacreacio = models.DateTimeField(db_column='DataCreacio', auto_now_add=True)
    datamodificacio = models.DateTimeField(db_column='DataModificacio', auto_now=True)

    class Meta:
        managed = False
        db_table = 'parroquia'
        verbose_name = "Parròquia"
        verbose_name_plural = "Parròquies"
        app_label = 'maestros'

    def __str__(self):
        return self.parroquia or "Parròquia"


class Poblacio(SafeSaveModel):
    id_poblacio = models.AutoField(primary_key=True)
    id_parroquia = models.ForeignKey(Parroquia, models.DO_NOTHING, db_column='id_parroquia', verbose_name="Parroquia",blank=False, null=False)
    poblacio = models.CharField(db_column='Poblacio', max_length=100, blank=False, null=False)
    codipostal = models.CharField(db_column='CodiPostal', max_length=100, blank=False, null=False)
    datacreacio = models.DateTimeField(db_column='DataCreacio', auto_now_add=True)
    datamodificacio = models.DateTimeField(db_column='DataModificacio', auto_now=True)


    class Meta:
        managed = False
        db_table = 'poblacio'
        verbose_name = "Població"
        verbose_name_plural = "Poblacions"
        app_label = 'maestros'

    def __str__(self):
        return self.poblacio or "Poblaci\u00f3"

class Recurso(SafeSaveModel):
    id_recurso = models.AutoField(primary_key=True)
    name = models.CharField(db_column='Name', max_length=100, blank=False, null=False)
    id_tipusrecurso = models.ForeignKey('Tipusrecurso', models.DO_NOTHING, db_column='id_tipusrecurso', blank=False, null=False)
    preutancat = models.IntegerField(db_column='PreuTancat', blank=False, null=False)
    preuhora = models.DecimalField(db_column='PreuHora', max_digits=10, decimal_places=2, blank=False, null=False)
    datacreacio = models.DateTimeField(db_column='DataCreacio', auto_now_add=True)
    datamodificacio = models.DateTimeField(db_column='DataModificacio', auto_now=True)


    class Meta:
        managed = False
        db_table = 'recurso'
        verbose_name = "Recurs"
        verbose_name_plural = "Recursos"
        app_label = 'maestros'

    def __str__(self):
        return self.name


class Tipusrecurso(SafeSaveModel):
    id_tipusrecurso = models.AutoField(primary_key=True)
    tipus = models.CharField(max_length=100, verbose_name="Tipus Recurs",blank=False, null=False)
    datacreacio = models.DateTimeField(db_column='DataCreacio', auto_now_add=True)
    datamodificacio = models.DateTimeField(db_column='DataModificacio', auto_now=True)


    class Meta:
        managed = False
        db_table = 'tipusrecurso'
        verbose_name = "Tipus de Recurs"
        verbose_name_plural = "Tipus de Recursos"
        app_label = 'maestros'

    def __str__(self):
        return self.tipus


class Tasca(SafeSaveModel):
    id_tasca = models.AutoField(primary_key=True)
    tasca = models.CharField(max_length=100, blank=False, null=False)
    observacions = models.TextField(blank=True, null=True)
    datacreacio = models.DateTimeField(db_column='data_creacio', auto_now_add=True)
    datamodificacio = models.DateTimeField(db_column='data_modificacio', auto_now=True)


    class Meta:
        managed = False
        db_table = 'tasca'
        verbose_name = "Tasca"
        verbose_name_plural = "Tasques"
        app_label = 'maestros'

    def __str__(self):
        return self.tasca[:30]


class Treballs(SafeSaveModel):
    id_treball = models.AutoField(primary_key=True)
    descripcio = models.CharField(max_length=100, blank=False, null=False)
    datacreacio = models.DateTimeField(db_column='data_creacio', auto_now_add=True)
    datamodificacio = models.DateTimeField(db_column='data_modificacio', auto_now=True)

    # Relación explícita ManyToMany con Tasca a través de TasquesTreball
    tasques = models.ManyToManyField(
        'Tasca',
        through='TasquesTreball',
        related_name='treballs'
    )

    class Meta:
        managed = False
        db_table = 'treballs'
        verbose_name = "Treball"
        verbose_name_plural = "Treballs"
        app_label = 'maestros'

    def __str__(self):
        return self.descripcio[:30]


class Ubicacio(SafeSaveModel):
    id_ubicacio = models.AutoField(primary_key=True)
    ubicacio = models.CharField("ubicacio", max_length=100, blank=False, null=False)
    datacreacio = models.DateTimeField(db_column='data_creacio', auto_now_add=True)
    datamodificacio = models.DateTimeField(db_column='data_modificacio', auto_now=True)


    class Meta:
        managed = False
        db_table = 'ubicacio'
        verbose_name = "Ubicació"
        verbose_name_plural = "Ubicacions"
        app_label = 'maestros'

    def __str__(self):
        return self.ubicacio[:30]


class Desplacaments(SafeSaveModel):
    id_desplacament = models.AutoField(primary_key=True)
    id_parroquia = models.ForeignKey(Parroquia, models.DO_NOTHING, db_column='id_parroquia', verbose_name="Parroquia", blank=False, null=False)
    id_ubicacio = models.ForeignKey(Ubicacio, models.DO_NOTHING, db_column='id_ubicacio', verbose_name="Ubicació",blank=False, null=False)
    id_tasca = models.ForeignKey(Tasca, models.DO_NOTHING, db_column='id_tasca', verbose_name="Tasca",blank=False, null=False)
    increment_hores = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Increment Hores",blank=False, null=False)
    observacions = models.TextField(blank=True, null=True)
    datacreacio = models.DateTimeField(db_column='data_creacio', auto_now_add=True)
    datamodificacio = models.DateTimeField(db_column='data_modificacio', auto_now=True)


    class Meta:
        managed = False
        db_table = 'desplacaments'
        verbose_name = "Desplaçament"
        verbose_name_plural = "Desplaçaments"
        app_label = 'maestros'

    def __str__(self):
        return f"Desplaçament {self.id_parroquia} - {self.id_tasca} ({self.id_parroquia})"    


class Hores(SafeSaveModel):
    id_hora = models.AutoField(primary_key=True)
    hores = models.DecimalField(max_digits=5, decimal_places=2, blank=False, null=False)
    datacreacio = models.DateTimeField(db_column='data_creacio', auto_now_add=True)
    datamodificacio = models.DateTimeField(db_column='data_modificacio', auto_now=True)


    class Meta:
        managed = False
        db_table = 'hores'
        verbose_name = "Hora"
        verbose_name_plural = "Hores"
        app_label = 'maestros'

    def __str__(self):
        return str(self.hores)


class TasquesTreball(SafeSaveModel):
    id_tasca_treball = models.AutoField(primary_key=True)
    id_tasca = models.ForeignKey(Tasca, models.DO_NOTHING, db_column='id_tasca', verbose_name="Tasca",blank=False, null=False)
    id_treball = models.ForeignKey(Treballs, models.DO_NOTHING, db_column='id_treball', verbose_name="Treball",blank=False, null=False)
    observacions = models.CharField("observacions", max_length=300, blank=True, null=True)
    datacreacio = models.DateTimeField(db_column='data_creacio', auto_now_add=True)
    datamodificacio = models.DateTimeField(db_column='data_modificacio', auto_now=True)


    class Meta:
        managed = False
        db_table = 'tasques_treball'
        unique_together = (('id_tasca', 'id_treball'),)
        verbose_name = "Traball - Tasca"
        verbose_name_plural = "Treballs - Tasques"
        app_label = 'maestros'

    def __str__(self):
        return f"{self.id_tasca} - {self.id_treball}"


class DepartamentClient(SafeSaveModel):
    id_departament = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100, verbose_name="Departament Client",blank=False, null=False)
    datacreacio = models.DateTimeField(db_column='data_creacio', auto_now_add=True)
    datamodificacio = models.DateTimeField(db_column='data_modificacio', auto_now=True)


    class Meta:
        managed = False
        db_table = 'departament_client'
        verbose_name = "Departament Client"
        verbose_name_plural = "Departaments Clients"
        app_label = 'maestros'

    def __str__(self):
        return self.nom
    
class PersonaContactClient(SafeSaveModel):
    id_persona_contact = models.AutoField(primary_key=True)
    id_client = models.ForeignKey(Clients, models.DO_NOTHING, db_column='id_client', verbose_name="Client",blank=False, null=False)
    nom_contacte = models.CharField(max_length=100, verbose_name = "Contacte Client",blank=False, null=False)
    telefon = telefon = PhoneNumberField("Telèfon",blank=True,null=True)
    datacreacio = models.DateTimeField(db_column='data_creacio', auto_now_add=True)
    datamodificacio = models.DateTimeField(db_column='data_modificacio', auto_now=True)


    class Meta:
        managed = False
        db_table = 'persona_contact_client'
        verbose_name = "Contacte Client"
        verbose_name_plural = "Contactes Client"
        app_label = 'maestros'

    def __str__(self):
        return self.nom_contacte



    
