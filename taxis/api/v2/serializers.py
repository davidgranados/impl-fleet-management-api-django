from rest_framework import serializers

from taxis.models import Taxi


class TaxiSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    plate = serializers.CharField(required=True, allow_blank=False, max_length=80)

    def create(self, validated_data):
        return Taxi.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.plate = validated_data.get('plate', instance.plate)
        instance.save()
        return instance
