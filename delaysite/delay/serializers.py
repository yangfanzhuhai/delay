from rest_framework import serializers
from delay.models import Bus_sequences


class PredictionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bus_sequences


class BusLineSerializer(serializers.Serializer):
    lineName = serializers.CharField(max_length=64)
    estimatedTime = serializers.ListField(child=serializers.CharField())


class StopSerializer(serializers.Serializer):
    stopPointName = serializers.CharField(max_length=64)
    latitude = serializers.DecimalField(max_digits=11, decimal_places=6)
    longitude = serializers.DecimalField(max_digits=11, decimal_places=6)
    lines = BusLineSerializer(many=True)


class ArrivalsSerializer(serializers.Serializer):
    stopPointName = serializers.CharField(max_length=64)
    latitude = serializers.DecimalField(max_digits=11, decimal_places=6)
    longitude = serializers.DecimalField(max_digits=11, decimal_places=6)
    lineName = serializers.CharField(max_length=64)
    estimatedTime = serializers.DateTimeField()
