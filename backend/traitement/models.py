from django.db import models
class Traitement(models.Model):
    dateDebut = models.DateField(null=True, blank=True)
    dateFin = models.DateField(null=True, blank=True)
    frequence = models.IntegerField(null=True, blank=True)
    instructionRepas = models.CharField(max_length=100, null=True, blank=True)
    medecament = models.ForeignKey('medicament.Medicament', on_delete=models.CASCADE, null=True, blank=True)
    paitent_id = models.ForeignKey('patient.Patient', on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.name if self.name else "Traitement"
# Create your models here.
