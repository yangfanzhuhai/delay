from rest_framework import serializers
from delay.models import Bus_sequences, Tfl_timetable


class PredictionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bus_sequences


class TflTimetableSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tfl_timetable


class BusLineSerializer(serializers.Serializer):
    route = serializers.CharField(max_length=64)
    stop_name = serializers.CharField(max_length=64)
    run = serializers.IntegerField()
    destination = serializers.CharField(max_length=64)
    estimatedTimeInSeconds = serializers.ListField(
        child=serializers.IntegerField()
    )


class StopSerializer(serializers.Serializer):
    stop_code_lbsl = serializers.CharField(max_length=16)
    sms_code = serializers.CharField(max_length=16)
    naptan_atco = serializers.CharField(max_length=64)
    latitude = serializers.DecimalField(max_digits=32, decimal_places=10)
    longitude = serializers.DecimalField(max_digits=32, decimal_places=10)
    lines = BusLineSerializer(many=True)
