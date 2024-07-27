from django.db import models
from account.models import CustomUser, Departement
from django.utils import timezone
from datetime import  date

def current_time():
    return timezone.now().time()

# Create your models here.
class Evaluation(models.Model):
    nom = models.CharField(max_length=128, default="", blank=True)
    dateDebut = models.DateField(max_length=128, default=date.today, blank=True)
    dateFin = models.DateField(max_length=128, default=date.today, blank=True)
    heureDebut = models.TimeField(max_length=128, default=current_time, blank=True)
    heureFin = models.TimeField(max_length=128, default=current_time, blank=True)
    departement = models.ForeignKey(Departement, on_delete=models.CASCADE, blank=True, related_name='departement_eval')

    def __str__(self):
        return self.nom

class Participe(models.Model):
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, related_name="participe")
    Departement = models.ForeignKey(Departement, on_delete=models.CASCADE, blank=True, related_name="participede")
    note = models.CharField(max_length=128, default="", blank=True)

    def __str__(self):
        return self.evaluation
        

class Question(models.Model):
    question = models.CharField(max_length=128, default="", blank=True)
    evaluations = models.ForeignKey(Evaluation, on_delete=models.CASCADE, blank=True, related_name='question')

    def __str__(self):
        return self.question


class Reponse(models.Model):
    bonneReponse = models.CharField(max_length=128, default="", blank=True)
    mauvaiseReponse = models.CharField(max_length=128, default="", blank=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, blank=True, related_name="reponse")

    def __str__(self):
        return self.bonneReponse 
