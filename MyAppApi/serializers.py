from rest_framework import serializers
from .models import Entities, Groups, Users, Number_List, Directory, Message


class EntitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entities
        fields = '__all__'


class GroupsSerializer(serializers.ModelSerializer):
    Entity = EntitiesSerializer()
    class Meta:
        model = Groups
        fields = '__all__'
        queryset = Entities.objects.all()


class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = '__all__'


class NumberListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Number_List
        fields = '__all__'


class DirectorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Directory
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
