from rest_framework import serializers
from delay.models import Bus_sequences


class PredictionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bus_sequences


class BusLineSerializer(serializers.Serializer):
    lineName = serializers.CharField(max_length=64)
    stopPointName = serializers.CharField(max_length=64)
    directionid = serializers.IntegerField()
    destination = serializers.CharField(max_length=64)
    estimatedTimeInSeconds = serializers.ListField(
        child=serializers.IntegerField()
    )


class StopSerializer(serializers.Serializer):
    stopid = serializers.CharField(max_length=16)
    stopcode1 = serializers.CharField(max_length=16)
    latitude = serializers.DecimalField(max_digits=11, decimal_places=6)
    longitude = serializers.DecimalField(max_digits=11, decimal_places=6)
    lines = BusLineSerializer(many=True)
