from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from evaluation.models import Evaluation, Participe, Question
from evaluation.serializer.serializer_in import EvaluationSerializer
from datetime import datetime


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
        evaluations = Evaluation.objects.filter(departement = user.departement).order_by("-id")
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
    question = Question.objects.all()
    
    