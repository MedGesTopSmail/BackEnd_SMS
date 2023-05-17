from rest_framework import serializers
from .models import Entities, Groups, Users, Number_List, Directory, Predefined_Message, Mailing_List, Relation_Directory_Number


class EntitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entities
        fields = '__all__'


class GroupsSerializer(serializers.ModelSerializer):
    Entity_Id = serializers.PrimaryKeyRelatedField(queryset=Entities.objects.all(), source='Entity', write_only=True)
    Entity = EntitiesSerializer(read_only=True)

    class Meta:
        model = Groups
        fields = '__all__'



class UsersSerializer(serializers.ModelSerializer):
    Group_Id = serializers.PrimaryKeyRelatedField(queryset=Groups.objects.all(), source='Group', write_only=True)
    Group = GroupsSerializer(read_only=True)
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


class RelationDirectoryNumberSerializer(serializers.ModelSerializer):
    Number_Id = serializers.PrimaryKeyRelatedField(queryset=Number_List.objects.all(), source='Number', write_only=True)
    Number = NumberListSerializer(read_only=True)

    Directory_Id = serializers.PrimaryKeyRelatedField(queryset=Directory.objects.all(), source='Directory', write_only=True)
    Directory = DirectorySerializer(read_only=True)

    class Meta:
        model = Relation_Directory_Number
        fields = '__all__'


class Mailing_ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mailing_List
        fields = '__all__'


class Predefined_MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Predefined_Message
        fields = '__all__'
