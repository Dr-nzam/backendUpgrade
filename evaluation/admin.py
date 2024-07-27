from django.contrib import admin
from evaluation.models import Evaluation, Participe, Question, Reponse,Departement

# Register your models here.

admin.site.register(Evaluation)
admin.site.register(Participe)
admin.site.register(Question)
admin.site.register(Reponse)
admin.site.register(Departement)

