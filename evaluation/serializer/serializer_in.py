from rest_framework import serializers
from account.serializer.serializer_in import UserSerializer
from evaluation.models import Evaluation, Question, Reponse,Participe
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
    departement = DepartementSerializer()
    reponse = ReponseSerializer(read_only=True, many = True)
    class Meta:
        model = Question
        fields = ['id','question','departement', 'reponse']

class ParticipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participe
        fields = '__all__'

class ParticipeSerializerOUT(serializers.ModelSerializer):
    evaluation = EvaluationSerializer()
    user = UserSerializer()
    departement = DepartementSerializer()
    class Meta:
        model = Participe
        fields = ['evaluation','user','departement','note',]

# class valideSerializer(serializers.ModelSerializer):
   #  serializers.CharField(required=True)



