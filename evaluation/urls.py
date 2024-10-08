from django.urls import path
from evaluation.vue.views import (newEvaluation, listEvaluationFuture,
                                   historiqueEvaluation,genererQuestion, 
                                   validerReponse, participe, statistique,listDepartement,
                                    verifierParticipation, suivis,generaleSuivis)

urlpatterns = [
    path('create-evaluation/', newEvaluation, name='register-user'),
    path('liste-evaluation-future/', listEvaluationFuture, name='liste-evaluation-future'),
    path('liste-evaluation-passe/', historiqueEvaluation, name='liste-evaluation-passe'),
    path('generer-question/', genererQuestion, name='generer-question'),
    path('valider-question/', validerReponse, name='valider-reponse'),
    path('participer-evaluation/', participe, name='participer-evaluation'),
    path('statistique-evaluation/', statistique, name='statistique-evaluation'),
    path('list-departement/', listDepartement, name='list-departement'),
    path('verification-participation/<int:pk>/', verifierParticipation, name='verification-participation'),
    path('suivis/', suivis, name='suivis'),
    path('generale-suivis/<int:pk>/', generaleSuivis, name='generale-suivis'),
]