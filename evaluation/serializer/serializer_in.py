from rest_framework import serializers
from evaluation.models import Evaluation, Question, Reponse
from account.models import Departement
# from account.models import Departement



class DepartementSerializer(serializers.ModelSerializer):
   class Meta:
        model = Departement
        fields = '__all__'

class EvaluationSerializer(serializers.ModelSerializer):
   class Meta:
        model = Evaluation
        fields = '__all__'

class ReponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reponse
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    evaluations = EvaluationSerializer()
    reponse = ReponseSerializer(many=True, read_only=True)
    class Meta:
        model = Question
        fields = ['id','question','evaluations','reponse']


# class valideSerializer(serializers.ModelSerializer):
   #  serializers.CharField(required=True)
    


