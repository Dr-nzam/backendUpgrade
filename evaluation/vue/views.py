from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from evaluation.models import Evaluation, Participe, Question, Departement, Reponse
from evaluation.serializer.serializer_in import (DepartementSerializer, EvaluationSerializer, ParticipeSerializer,
                                                  QuestionSerializer, ParticipeSerializerOUT)
from datetime import datetime
import random
import statistics 
from django.db.models import Q

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def newEvaluation(request):
    user = request.user
    if user.is_admin:
        serializer = EvaluationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Evaluation ajouter avec succès','data':serializer.data},
                             status=status.HTTP_201_CREATED)
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
            dateConvert = datetime.strptime(evaluation.dateDebut, "%d/%m/%Y").date()
            if dateConvert >= dateActuelle:
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
            dateConvert = datetime.strptime(evaluation.dateDebut, "%d/%m/%Y").date()
            if dateConvert < dateActuelle:
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
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def participe(request):
    data = request.data
    user = request.user
    idEvent  = data.get('id_event')
    idDepartement  = data.get('id_departement')
    note = data.get('note')
    if Participe.objects.filter(Q(user = user) & Q(evaluation =idEvent)).exists():
        return Response({"messsage":"Vous avez deja participez"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        dataInfo = {'evaluation': idEvent, 'user': user.id, 'departement':idDepartement, 'note':note }
        serializer = ParticipeSerializer(data= dataInfo)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def statistique(request):
    user = request.user
    listNote = []
    if user.is_admin:
        participation = Participe.objects.all().order_by("-id")
        evaluations = set(participation.values_list('evaluation', flat=True))
        serializer = []
        for evaluation in evaluations:
            participation_evaluation = participation.filter(evaluation=evaluation)
            listNote = [participe.note for participe in participation_evaluation]
            listNote.sort()
            moyenne = statistics.mean(listNote)
            petiteNote = min(listNote)
            premiereNote = max(listNote)
            serializer.append({
                "evaluation": evaluation,
                "participations": ParticipeSerializerOUT(participation_evaluation, many=True).data,
                "moyenne": moyenne,
                "petite_note": petiteNote,
                "premiereNote": premiereNote
            })
        return Response(serializer, status=status.HTTP_200_OK)
    else:
        participation = Participe.objects.filter(user=user.id).order_by("-id")
        evaluations = set(participation.values_list('evaluation', flat=True))
        serializer = []
        for evaluation in evaluations:
            participation_evaluation = participation.filter(evaluation=evaluation)
            listNote = [participe.note for participe in participation_evaluation]
            listNote.sort()
            moyenne = statistics.mean(listNote)
            petiteNote = min(listNote)
            premiereNote = max(listNote)
            serializer.append({
                "evaluation": evaluation,
                "participations": ParticipeSerializerOUT(participation_evaluation, many=True).data,
                "moyenne": moyenne,
                "petite_note": petiteNote,
                "premiereNote": premiereNote
            })
        return Response(serializer, status=status.HTTP_200_OK)  
    


@api_view()
@permission_classes([IsAuthenticated])
def listDepartement(request):
    user = request.user
    if user.is_admin:
        departement = Departement.objects.all()
        serializer = DepartementSerializer(departement, many=True).data
        return Response(serializer, status=status.HTTP_200_OK)
    return Response({"message":"vous n'avez pas les droits"}, status=status.HTTP_200_OK)
