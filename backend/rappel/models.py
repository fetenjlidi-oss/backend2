from django.db import models
class Rappel(models.Model):
    heure = models.DateTimeField(null=True, blank=True)
    heurePrevue = models.DateTimeField(null=True, blank=True)
    estConfirme= models.BooleanField(default=False)
    delaiSnooze = models.IntegerField(null=True, blank=True)
    isSnoozed = models.BooleanField(default=False)
    traitement = models.ForeignKey('traitement.Traitement', on_delete=models.CASCADE, related_name='rappels')
    def __str__(self):
        return f"Rappel for {self.medicament.name} at {self.time}"
# Create your models here.
