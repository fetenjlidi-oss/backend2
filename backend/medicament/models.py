from django.db import models

class Medicament(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    dosage_ref = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    unity = models.CharField(max_length=50, null=True, blank=True)
    time= models.DateTimeField(null=True, blank=True)
    time_takes= models.DateTimeField(null=True, blank=True)
    quantity_total= models.IntegerField(null=True, blank=True)
    quantity_limit= models.IntegerField(null=True, blank=True)
    date_start = models.DateField(null=True, blank=True)
    date_end = models.DateField(null=True, blank=True)
    image=  models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name if self.name else "Medicament"
# Create your models here.
