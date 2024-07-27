from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from evaluation.models import Evaluation, Participe, Question, Departement, Reponse
from evaluation.serializer.serializer_in import EvaluationSerializer, QuestionSerializer
from datetime import datetime
import random


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def newEvaluation(request):
    user = request.user
    if user.is_admin:
        serializer = EvaluationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"message": "vous n'avez pas l'autorisation pour effectuer cette action."},
                         status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listEvaluationFuture(request):
    user = request.user
    dateActuelle = datetime.now().date()
    listeEvaluations = []
    if user.is_admin:
        evaluations = Evaluation.objects.all().order_by("-id")
        for evaluation in evaluations:
            if evaluation.dateDebut >= dateActuelle:
                listeEvaluations.append(evaluation)
        serializer = EvaluationSerializer(listeEvaluations, many=True).data
        return Response(serializer, status=status.HTTP_200_OK)
    else:
        idDepartementUser = user.departement.id
        departement = Departement.objects.get(id = idDepartementUser)
        evaluations = Evaluation.objects.filter(departement = departement.id).order_by("-id")
        for evaluation in evaluations:
            if evaluation.dateDebut >= dateActuelle:
                listeEvaluations.append(evaluation)
        serializer = EvaluationSerializer(listeEvaluations, many=True).data
        return Response(serializer, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def historiqueEvaluation(request):
    user = request.user
    dateActuelle = datetime.now().date()
    listeEvaluations = []
    if user.is_admin:
        evaluations = Evaluation.objects.all().order_by("-id")
        for evaluation in evaluations:
            if evaluation.dateDebut < dateActuelle:
                listeEvaluations.append(evaluation)
        serializer = EvaluationSerializer(listeEvaluations, many=True).data
        return Response(serializer, status=status.HTTP_200_OK)
    else:
        # idDepartementUser = user.departement.id
        participations  = Participe.objects.filter(user = user.id)
        for participation in participations:
            evaluations = Evaluation.objects.get(id = participation.evaluation.id)
            listeEvaluations.append(evaluations)
        serializer = EvaluationSerializer(listeEvaluations, many = True).data
        return Response(serializer, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def genererQuestion(request):
    user = request.user
    idDepartementUser = user.departement.id
    # dateActuelle = datetime.now().date()
    # heureActuelle = datetime.now().time()
    departement = Departement.objects.get(id = idDepartementUser)
    evaluations = Evaluation.objects.filter(departement = departement.id)
    questionList = []
    print(evaluations)
    if len(evaluations) != 0:
        for evaluation in evaluations:
            questions = Question.objects.filter(evaluations = evaluation.id)
            if len(questions)!=0:
                for question in questions:
                    questionList.append(question)
            else:
                return Response({"message": f"Aucune question n'est disponible pour l'evaluation {evaluation.nom}"},
                         status=status.HTTP_400_BAD_REQUEST)
        random.shuffle(questionList)
        serializer = QuestionSerializer(questionList, many = True).data
        return Response(serializer, status=status.HTTP_200_OK)
    else:
        return Response({"message": f"Aucune evaluation n'est disponible pour le departement {departement.nomDepartement}"},
                         status=status.HTTP_400_BAD_REQUEST)
    


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def validerReponse(request):
    data = request.data
    idQuestion = data['id_question']
    reponseUser = data['reponse']
    reponse = Reponse.objects.get(question = idQuestion)
    if(reponse.bonneReponse == reponseUser):
        return Response({"message":"bonne reponse"}, status=status.HTTP_200_OK)
    else:
        return Response({"message":"mauvaise reponse"}, status=status.HTTP_400_BAD_REQUEST)