from rest_framework import serializers
from .models import Entities, Groups, Users, Number_List, Directory, Message


class EntitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entities
        fields = '__all__'


class GroupsSerializer(serializers.ModelSerializer):
    Entity_Id = serializers.PrimaryKeyRelatedField(queryset=Entities.objects.all(), source='Entity', write_only=True)
    Entity = EntitiesSerializer(read_only=True)

    class Meta:
        model = Groups
        fields = ('Group_Id', 'Group_Number', 'Group_Name', 'Group_Description', 'Entity_Id', 'Entity')



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
