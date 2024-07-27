from django.urls import path
from evaluation.vue.views import (newEvaluation, listEvaluationFuture,
                                   historiqueEvaluation,genererQuestion, validerReponse)

urlpatterns = [
    path('create-evaluation/', newEvaluation, name='register-user'),
    path('liste-evaluation-future/', listEvaluationFuture, name='liste-evaluation-future'),
    path('liste-evaluation-passe/', historiqueEvaluation, name='liste-evaluation-passe'),
    path('generer-question/', genererQuestion, name='generer-question'),
    path('valider-question/', validerReponse, name='valider-reponse')
    
]