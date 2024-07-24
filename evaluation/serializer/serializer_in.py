from rest_framework import serializers
from evaluation.models import Evaluation

class EvaluationSerializer(serializers.ModelSerializer):
   class Meta:
        model = Evaluation
        fields = '__all__'