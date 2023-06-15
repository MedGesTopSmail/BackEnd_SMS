from rest_framework import serializers
from .models import Entities, Groups, Users, Number_List, Directory, Predefined_Message, Mailing_List, \
    Relation_Directory_Number, Log_Message, Email_To_Sms, Permission_User, Permissions, Roles, Role_User


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

    Directory_Id = serializers.PrimaryKeyRelatedField(queryset=Directory.objects.all(), source='Directory',
                                                      write_only=True)
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


class Log_MessageSerializer(serializers.ModelSerializer):
    User_Id = serializers.PrimaryKeyRelatedField(queryset=Users.objects.all(), source='User', write_only=True)
    User = UsersSerializer(read_only=True)

    class Meta:
        model = Log_Message
        fields = '__all__'


class Email_To_SmsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email_To_Sms
        fields = '__all__'


class PermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permissions
        fields = '__all__'


class Permission_UserSerializer(serializers.ModelSerializer):
    Id = serializers.PrimaryKeyRelatedField(queryset=Permissions.objects.all(), source='Permissions', write_only=True)
    Permission = PermissionsSerializer(read_only=True)

    User_Id = serializers.PrimaryKeyRelatedField(queryset=Users.objects.all(), source='User', write_only=True)
    User = UsersSerializer(read_only=True)

    class Meta:
        model = Permission_User
        fields = '__all__'


class RolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = '__all__'


class Role_UserSerializer(serializers.ModelSerializer):
    Id = serializers.PrimaryKeyRelatedField(queryset=Roles.objects.all(), source='Roles', write_only=True)
    Role = RolesSerializer(read_only=True)

    User_Id = serializers.PrimaryKeyRelatedField(queryset=Users.objects.all(), source='User', write_only=True)
    User = UsersSerializer(read_only=True)

    class Meta:
        model = Role_User
        fields = '__all__'
