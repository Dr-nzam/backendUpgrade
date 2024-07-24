from django.db import models
from account.models import CustomUser

# Create your models here.
class Evaluation(models.Model):
    nom = models.CharField(max_length=128, default="", blank=True)
    dateDebut = models.DateField(max_length=128, default="", blank=True)
    dateFin = models.DateField(max_length=128, default="", blank=True)
    heureDebut = models.TimeField(max_length=128, default="", blank=True)
    heureFin = models.TimeField(max_length=128, default="", blank=True)
    departement = models.CharField(max_length=128, default="", blank=True)

    def __str__(self):
        return self.nom

class Participe(models.Model):
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True)

class Question(models.Model):
    question = models.CharField(max_length=128, default="", blank=True)
    Evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE, blank=True)

class Reponse(models.Model):
    bonneReponse = models.CharField(max_length=128, default="", blank=True)
    mauvaiseReponse = models.CharField(max_length=128, default="", blank=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, blank=True)