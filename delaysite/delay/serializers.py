from rest_framework import serializers
from delay.models import Bus_sequences


class PredictionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bus_sequences
