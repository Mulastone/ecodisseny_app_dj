from django.db import models


from django.db import models

class Clients(models.Model):
    id_client = models.AutoField(primary_key=True, verbose_name="ID")

    nomclient = models.CharField("Nom del Client", max_length=100, blank=True, null=True)
    rsocial = models.CharField("Raó Social", max_length=100, blank=True, null=True)
    nrt = models.CharField("NRT", max_length=100, blank=True, null=True)

    parroquia = models.ForeignKey(
        'Parroquia', 
        models.DO_NOTHING, 
        blank=True, 
        null=True, 
        verbose_name="Parròquia"
    )

    poblacio = models.ForeignKey(
        'Poblacio', 
        models.DO_NOTHING, 
        blank=True, 
        null=True, 
        verbose_name="Població"
    )

    carrer = models.CharField("Carrer", max_length=100, blank=True, null=True)
    nro = models.CharField("Número", max_length=100, blank=True, null=True)
    escala = models.CharField("Escala", max_length=100, blank=True, null=True)
    pis = models.IntegerField("Pis", blank=True, null=True)
    porta = models.CharField("Porta", max_length=100, blank=True, null=True)
    telefon = models.CharField("Telèfon", max_length=100, blank=True, null=True)
    mail = models.CharField("Correu electrònic", max_length=100, blank=True, null=True)

    datacreacio = models.DateTimeField(db_column='DataCreacio', auto_now_add=True)
    datamodificacio = models.DateTimeField(db_column='DataModificacio', auto_now=True)



    class Meta:
        managed = False
        db_table = 'clients'
        verbose_name = "Client"
        verbose_name_plural = "Clients"

    def __str__(self):
        return self.nomclient or "Client sense nom"




class Parroquia(models.Model):
    id_parroquia = models.AutoField(primary_key=True)
    parroquia = models.CharField(db_column='Parroquia', max_length=100, blank=True, null=True)
    datacreacio = models.DateTimeField(db_column='DataCreacio', auto_now_add=True)
    datamodificacio = models.DateTimeField(db_column='DataModificacio', auto_now=True)



    class Meta:
        managed = False
        db_table = 'parroquia'
        verbose_name = "Parròquia"
        verbose_name_plural = "Parròquies"

    def __str__(self):
        return self.parroquia or "Parr\u00f2quia"


class Poblacio(models.Model):
    id_poblacio = models.AutoField(primary_key=True)
    id_parroquia = models.ForeignKey(Parroquia, models.DO_NOTHING, db_column='id_parroquia', blank=True, null=True)
    poblacio = models.CharField(db_column='Poblacio', max_length=100, blank=True, null=True)
    codipostal = models.CharField(db_column='CodiPostal', max_length=100, blank=True, null=True)
    datacreacio = models.DateTimeField(db_column='DataCreacio', auto_now_add=True)
    datamodificacio = models.DateTimeField(db_column='DataModificacio', auto_now=True)


    class Meta:
        managed = False
        db_table = 'poblacio'
        verbose_name = "Població"
        verbose_name_plural = "Poblacions"

    def __str__(self):
        return self.poblacio or "Poblaci\u00f3"

class Recurso(models.Model):
    id_recurso = models.AutoField(primary_key=True)
    name = models.CharField(db_column='Name', max_length=100)
    id_tipusrecurso = models.ForeignKey('Tipusrecurso', models.DO_NOTHING, db_column='id_tipusrecurso', blank=True, null=True)
    preutancat = models.IntegerField(db_column='PreuTancat', blank=True, null=True)
    preuhora = models.DecimalField(db_column='PreuHora', max_digits=10, decimal_places=4, blank=True, null=True)
    datacreacio = models.DateTimeField(db_column='DataCreacio', auto_now_add=True)
    datamodificacio = models.DateTimeField(db_column='DataModificacio', auto_now=True)


    class Meta:
        managed = False
        db_table = 'recurso'
        verbose_name = "Recurs"
        verbose_name_plural = "Recursos"

    def __str__(self):
        return self.name


class Tipusrecurso(models.Model):
    id_tipusrecurso = models.AutoField(primary_key=True)
    tipus = models.CharField(max_length=100)
    datacreacio = models.DateTimeField(db_column='DataCreacio', auto_now_add=True)
    datamodificacio = models.DateTimeField(db_column='DataModificacio', auto_now=True)


    class Meta:
        managed = False
        db_table = 'tipusrecurso'
        verbose_name = "Tipus de Recurs"
        verbose_name_plural = "Tipus de Recursos"

    def __str__(self):
        return self.tipus


class Tasca(models.Model):
    id_tasca = models.AutoField(primary_key=True)
    tasca = models.TextField()
    observacions = models.TextField(blank=True, null=True)
    datacreacio = models.DateTimeField(db_column='data_creacio', auto_now_add=True)
    datamodificacio = models.DateTimeField(db_column='data_modificacio', auto_now=True)


    class Meta:
        managed = False
        db_table = 'tasca'
        verbose_name = "Tasca"
        verbose_name_plural = "Tasques"

    def __str__(self):
        return self.tasca[:30]


class Treballs(models.Model):
    id_treball = models.AutoField(primary_key=True)
    descripcio = models.TextField()
    datacreacio = models.DateTimeField(db_column='data_creacio', auto_now_add=True)
    datamodificacio = models.DateTimeField(db_column='data_modificacio', auto_now=True)


    class Meta:
        managed = False
        db_table = 'treballs'
        verbose_name = "Treball"
        verbose_name_plural = "Treballs"

    def __str__(self):
        return self.descripcio[:30]


class Ubicacio(models.Model):
    id_ubicacio = models.AutoField(primary_key=True)
    ubicacio = models.CharField("ubicacio", max_length=100, blank=True, null=True)
    datacreacio = models.DateTimeField(db_column='data_creacio', auto_now_add=True)
    datamodificacio = models.DateTimeField(db_column='data_modificacio', auto_now=True)


    class Meta:
        managed = False
        db_table = 'ubicacio'
        verbose_name = "Ubicació"
        verbose_name_plural = "Ubicacions"

    def __str__(self):
        return self.ubicacio[:30]


class Desplacaments(models.Model):
    id_desplacament = models.AutoField(primary_key=True)
    id_parroquia = models.ForeignKey(Parroquia, models.DO_NOTHING, db_column='id_parroquia')
    id_ubicacio = models.ForeignKey(Ubicacio, models.DO_NOTHING, db_column='id_ubicacio')
    id_tasca = models.ForeignKey(Tasca, models.DO_NOTHING, db_column='id_tasca')
    increment_hores = models.DecimalField(max_digits=5, decimal_places=2)
    observacions = models.TextField(blank=True, null=True)
    datacreacio = models.DateTimeField(db_column='data_creacio', auto_now_add=True)
    datamodificacio = models.DateTimeField(db_column='data_modificacio', auto_now=True)


    class Meta:
        managed = False
        db_table = 'desplacaments'
        verbose_name = "Desplaçament"
        verbose_name_plural = "Desplaçaments"

    def __str__(self):
        return f"Desplaçament {self.id_parroquia} - {self.id_tasca} ({self.id_parroquia})"    


class Hores(models.Model):
    id_hora = models.AutoField(primary_key=True)
    hores = models.DecimalField(max_digits=5, decimal_places=2)
    datacreacio = models.DateTimeField(db_column='data_creacio', auto_now_add=True)
    datamodificacio = models.DateTimeField(db_column='data_modificacio', auto_now=True)


    class Meta:
        managed = False
        db_table = 'hores'
        verbose_name = "Hora"
        verbose_name_plural = "Hores"

    def __str__(self):
        return str(self.hores)


class TasquesTreball(models.Model):
    id_tasca_treball = models.AutoField(primary_key=True)
    id_tasca = models.ForeignKey(Tasca, models.DO_NOTHING, db_column='id_tasca')
    id_treball = models.ForeignKey(Treballs, models.DO_NOTHING, db_column='id_treball')
    observacions = models.TextField(blank=True, null=True)
    datacreacio = models.DateTimeField(db_column='data_creacio', auto_now_add=True)
    datamodificacio = models.DateTimeField(db_column='data_modificacio', auto_now=True)


    class Meta:
        managed = False
        db_table = 'tasques_treball'
        unique_together = (('id_tasca', 'id_treball'),)
        verbose_name = "Traball - Tasca"
        verbose_name_plural = "Treballs - Tasques"

    def __str__(self):
        return f"{self.id_tasca} - {self.id_treball}"


class DepartamentClient(models.Model):
    id_departament = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    datacreacio = models.DateTimeField(db_column='data_creacio', auto_now_add=True)
    datamodificacio = models.DateTimeField(db_column='data_modificacio', auto_now=True)


    class Meta:
        managed = False
        db_table = 'departament_client'
        verbose_name = "Departament Client"
        verbose_name_plural = "Departaments Clients"

    def __str__(self):
        return self.nom
class PersonaContactClient(models.Model):
    id_persona_contact = models.AutoField(primary_key=True)
    id_client = models.ForeignKey(Clients, models.DO_NOTHING, db_column='id_client')
    nom_contacte = models.CharField(max_length=100)
    datacreacio = models.DateTimeField(db_column='data_creacio', auto_now_add=True)
    datamodificacio = models.DateTimeField(db_column='data_modificacio', auto_now=True)


    class Meta:
        managed = False
        db_table = 'persona_contact_client'
        verbose_name = "Persona de contacte del client"
        verbose_name_plural = "Persones de contacte del client"

    def __str__(self):
        return self.nom_contacte


class Projectes(models.Model):
    id_projecte = models.AutoField(primary_key=True)
    nom_projecte = models.CharField(max_length=255)
    data_peticio = models.DateTimeField(blank=True, null=True)
    id_client = models.ForeignKey(Clients, models.DO_NOTHING, db_column='id_client')
    id_departament = models.ForeignKey(DepartamentClient, models.DO_NOTHING, db_column='id_departament')
    id_persona_contact = models.ForeignKey(PersonaContactClient, models.DO_NOTHING, db_column='id_persona_contact')
    id_parroquia = models.ForeignKey(Parroquia, models.DO_NOTHING, db_column='id_parroquia')
    id_ubicacio = models.ForeignKey(Ubicacio, models.DO_NOTHING, db_column='id_ubicacio')
    observacions = models.TextField(blank=True, null=True)
    tancat = models.IntegerField(blank=True, null=True)
    datacreacio = models.DateTimeField(db_column='data_creacio', auto_now_add=True)
    datamodificacio = models.DateTimeField(db_column='data_modificacio', auto_now=True)


    class Meta:
        managed = False
        db_table = 'projectes'
        verbose_name = "Projecte"
        verbose_name_plural = "Projectes"
        
    def __str__(self):
        return self.nom_projecte
    
class Pressupostos(models.Model):
    id_pressupost = models.AutoField(primary_key=True)
    id_projecte = models.ForeignKey(Projectes, models.DO_NOTHING, db_column='id_projecte')
    id_parroquia = models.ForeignKey(Parroquia, models.DO_NOTHING, db_column='id_parroquia')
    id_ubicacio = models.ForeignKey(Ubicacio, models.DO_NOTHING, db_column='id_ubicacio')
    nom_pressupost = models.CharField(max_length=255)
    data_pressupost = models.DateTimeField(blank=True, null=True)
    id_client = models.ForeignKey(Clients, models.DO_NOTHING, db_column='id_client')
    observacions = models.TextField(blank=True, null=True)
    tancat = models.IntegerField(blank=True, null=True)
    datacreacio = models.DateTimeField(db_column='data_creacio', auto_now_add=True)
    datamodificacio = models.DateTimeField(db_column='data_modificacio', auto_now=True)


    class Meta:
        managed = False
        db_table = 'pressupostos'
        verbose_name = "Pressupost"
        verbose_name_plural = "Presuspostos"

    def __str__(self):
        return f"{self.nom_pressupost} ({self.id_projecte})"


class PressupostosLineas(models.Model):
    id_pressupost_linea = models.AutoField(primary_key=True)
    id_pressupost = models.ForeignKey(Pressupostos, models.DO_NOTHING, db_column='id_pressupost')
    id_treball = models.ForeignKey(Treballs, models.DO_NOTHING, db_column='id_treball')
    id_tasca = models.ForeignKey(Tasca, models.DO_NOTHING, db_column='id_tasca')
    quantitat = models.IntegerField()
    id_recurso = models.ForeignKey(Recurso, models.DO_NOTHING, db_column='id_recurso')
    preu_tancat = models.IntegerField(blank=True, null=True)
    cost_tancat = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    id_hora = models.ForeignKey(Hores, models.DO_NOTHING, db_column='id_hora', blank=True, null=True)
    increment_hores = models.DecimalField(max_digits=5, decimal_places=2)
    hores_totales = models.DecimalField(max_digits=5, decimal_places=2)
    cost_hores = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    cost_hores_totals = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    subtotal_linea = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    benefici_linea = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    total_linea = models.DecimalField(max_digits=10, decimal_places=4, blank=True, null=True)
    datacreacio = models.DateTimeField(db_column='data_creacio', auto_now_add=True)
    datamodificacio = models.DateTimeField(db_column='data_modificacio', auto_now=True)


    class Meta:
        managed = False
        db_table = 'pressupostos_lineas'
        verbose_name = "Pressuost Linea"
        verbose_name_plural = "Pessupostos Linees"

    def __str__(self):
        return f"L\u00ednea {self.id_pressupost_linea} - Pressupost {self.id_pressupost_id}"
    

