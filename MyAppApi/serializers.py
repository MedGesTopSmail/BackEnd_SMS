from rest_framework import serializers
from .models import Entities


class EntitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entities
        fields = '__all__'

