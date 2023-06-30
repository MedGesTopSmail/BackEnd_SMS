import os
import sys
import csv
import ast
import pytz
import time
# import gammu
import base64
import random
import tempfile
import subprocess
from . import serializers
from crontab import CronTab
from django.contrib import auth
from django.db import connection
from Project_SMS import settings
from rest_framework import status
from django.utils import timezone
from django.db.models import Count
from django.http import JsonResponse
from datetime import datetime, timedelta
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.core.management import call_command
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from .serializers import Mailing_ListSerializer, Log_MessageSerializer, Permission_UserSerializer, Role_UserSerializer, \
    MonitoringSerializer
from .models import Entities, Groups, Users, Number_List, Directory, Predefined_Message, Mailing_List, Monitoring, \
    Relation_Directory_Number, Log_Message, Email_To_Sms, Permission_User, Permissions, Roles, Role_User

#### Config Files ####


CONFIG_CONTENT_1 = """
[gammu]
port = /dev/ttyUSB3
model = at
connection = at115200
synchronizetime = yes
logformat = nothing
use_locking =
gammuloc =

[smsd]
HangupCalls=1
CheckBattery=0
CheckSecurity=0
logfile = /home/mysms/backend/addon/logs/gammu/modem-1
commtimeout = 10
sendtimeout = 10
logformat = textalldate
Receive=0
deliveryreport = sms
phoneid = 1
debuglevel = 255
Service = sql
Driver = native_mysql
User = mysms
Password = P@SsW0rd
host = localhost
Database = smsdb
"""

CONFIG_CONTENT_2 = """
[gammu]
port = /dev/ttyUSB7
model = at
connection = at115200
synchronizetime = yes
logformat = nothing
use_locking =
gammuloc =

[smsd]
HangupCalls=1
CheckBattery=0
CheckSecurity=0
logfile = /home/mysms/backend/addon/logs/gammu/modem-2
commtimeout = 10
sendtimeout = 10
logformat = textalldate
Receive=0
deliveryreport = sms
phoneid = 2
debuglevel = 255
Service = sql
Driver = native_mysql
User = mysms
Password = P@SsW0rd
host = localhost
Database = smsdb
"""

CONFIG_CONTENT_3 = """
[gammu]
port = /dev/ttyUSB11
model = at
connection = at115200
synchronizetime = yes
logformat = nothing
use_locking =
gammuloc =

[smsd]
HangupCalls=1
CheckBattery=0
CheckSecurity=0
logfile = /home/mysms/backend/addon/logs/gammu/modem-3
commtimeout = 10
sendtimeout = 10
logformat = textalldate
Receive=0
deliveryreport = sms
phoneid = 3
debuglevel = 255
Service = sql
Driver = native_mysql
User = mysms
Password = P@SsW0rd
host = localhost
Database = smsdb
"""

CONFIG_CONTENT_4 = """
[gammu]
port = /dev/ttyUSB15
model = at
connection = at115200
synchronizetime = yes
logformat = nothing
use_locking =
gammuloc =

[smsd]
HangupCalls=1
CheckBattery=0
CheckSecurity=0
logfile = /home/mysms/backend/addon/logs/gammu/modem-4
commtimeout = 10
sendtimeout = 10
logformat = textalldate
Receive=0
deliveryreport = sms
phoneid = 4
debuglevel = 255
Service = sql
Driver = native_mysql
User = mysms
Password = P@SsW0rd
host = localhost
Database = smsdb
"""


#### End Config Files ####


def index(request):
    return render(request, 'index.html')


class DashboardDetail(APIView):
    def get(self, request):
        modem_counts = Log_Message.objects.values('Modem').annotate(count=Count('Modem'))
        modem_count_list = [{'modem': f'Modem{item["Modem"]}', 'count': item['count']} for item in modem_counts]
        return JsonResponse(modem_count_list, safe=False)



def generate(self, tag):
    if tag.upper() == "ENT":
        Entity_Number = tag.upper() + f'{random.randint(0, 9999):04}'
        while Entities.objects.filter(Entity_Number=Entity_Number).exists():
            Entity_Number = tag.upper() + f'{random.randint(0, 9999):04}'
        data = {
            "Entity_Number": Entity_Number,
        }
        return JsonResponse(data)
    elif tag.upper() == "GR":
        Group_Number = tag.upper() + f'{random.randint(0, 9999):04}'
        while Groups.objects.filter(Group_Number=Group_Number).exists():
            Group_Number = tag.upper() + f'{random.randint(0, 9999):04}'
        data = {
            "Group_Number": Group_Number,
        }
        return JsonResponse(data)
    elif tag.upper() == "USR":
        User_Number = tag.upper() + f'{random.randint(0, 9999):04}'
        while Users.objects.filter(User_Number=User_Number).exists():
            User_Number = tag.upper() + f'{random.randint(0, 9999):04}'
        data = {
            "User_Number": User_Number,
        }
        return JsonResponse(data)
    elif tag.upper() == "DRC":
        Directory_Number = tag.upper() + f'{random.randint(0, 9999):04}'
        while Directory.objects.filter(Directory_Number=Directory_Number).exists():
            Directory_Number = tag.upper() + f'{random.randint(0, 9999):04}'
        data = {
            "Directory_Number": Directory_Number,
        }
        return JsonResponse(data)


# CRUD Entities
class EntitiesDetail(APIView):
    def get(self, request):
        obj = Entities.objects.filter(deleted_by__isnull=True)
        serializer = serializers.EntitiesSerializer(obj, many=True)
        data = serializer.data
        return JsonResponse(data, safe=False)

    def post(self, request):
        serializer = serializers.EntitiesSerializer(data=request.data)
        if serializer.is_valid():
            entity_name = serializer.validated_data['Entity_Name']
            if Entities.objects.filter(Entity_Name=entity_name).filter(deleted_by__isnull=True).exists():
                message = {
                    "type": "error",
                    "message": "Entité " + entity_name + " existe deja",
                }
                return JsonResponse(message)
            serializer.save()
            data = serializer.data
            message = {
                "type": "success",
                "message": "Entité " + data.get("Entity_Name") + " ajouter avec succes",
                "id": data.get("Entity_Id")
            }
            return JsonResponse(message)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EntitiesInfo(APIView):
    def get(self, request, id):
        try:
            obj = Entities.objects.filter(deleted_by__isnull=True).get(Entity_Id=id)
            serializer = serializers.EntitiesSerializer(obj)
            data = serializer.data
            return JsonResponse(data, safe=False)
        except Entities.DoesNotExist:
            message = {"message": "Entité non trouver"}
            return JsonResponse(message, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id):
        try:
            obj = Entities.objects.filter(deleted_by__isnull=True).get(Entity_Id=id)
            serializer = serializers.EntitiesSerializer(obj, data=request.data)
            if serializer.is_valid():
                entity_name = serializer.validated_data['Entity_Name']
                if obj.Entity_Name != request.data['Entity_Name']:
                    if Entities.objects.filter(Entity_Name=entity_name).filter(deleted_by__isnull=True).exists():
                        message = {
                            "type": "error",
                            "message": "Entité " + entity_name + " existe deja",
                        }
                        return JsonResponse(message)
                serializer.save()
                data = serializer.data
                message = {
                    "type": "success",
                    "message": "Entité " + data.get("Entity_Name") + " modifier avec succes",
                    "id": data.get("Entity_Id")
                }
                return JsonResponse(message)
        except Entities.DoesNotExist:
            message = {"message": "Entité non trouver"}
            return JsonResponse(message, status=status.HTTP_404_NOT_FOUND)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id):
        try:
            obj = Entities.objects.filter(deleted_by__isnull=True).get(Entity_Id=id)
            serializer = serializers.EntitiesSerializer(obj, data=request.data, partial=True)
            if serializer.is_valid():
                entity_name = serializer.validated_data['Entity_Name']
                if obj.Entity_Name != request.data['Entity_Name']:
                    if Entities.objects.filter(Entity_Name=entity_name).filter(deleted_by__isnull=True).exists():
                        message = {
                            "type": "error",
                            "message": "Entité " + entity_name + " existe deja",
                        }
                        return JsonResponse(message)
                serializer.save()
                data = serializer.data
                message = {
                    "type": "success",
                    "message": "Entité " + data.get("Entity_Name") + " modifier avec succes",
                    "id": data.get("Entity_Id")
                }
                return JsonResponse(message)
        except Entities.DoesNotExist:
            message = {"message": "Entity not found"}
            return JsonResponse(message, status=status.HTTP_404_NOT_FOUND)

    @csrf_exempt
    def delete(self, request, id):
        try:
            obj = Entities.objects.get(Entity_Id=id)
            name = obj.Entity_Name
            obj.deleted_at = timezone.now()
            obj.deleted_by = 1
            obj.save()
            message = {
                "type": "success",
                "message": "Entite " + name + " Supprimer avec succes",
            }
            return JsonResponse(message)
        except Entities.DoesNotExist:
            message = {"message": "Entity not found"}
            return JsonResponse(message, status=status.HTTP_404_NOT_FOUND)


# CRUD Groups
class GroupsDetail(APIView):
    queryset = Groups.objects.filter(deleted_by__isnull=True).all()

    def get(self, request):
        obj_groups = self.queryset.all()
        serializer = serializers.GroupsSerializer(obj_groups, many=True)
        data = serializer.data
        return JsonResponse(data, safe=False)

    def post(self, request):
        serializer = serializers.GroupsSerializer(data=request.data)
        if serializer.is_valid():
            group_name = serializer.validated_data['Group_Name']
            if Groups.objects.filter(Group_Name=group_name).filter(deleted_by__isnull=True).exists():
                message = {
                    "type": "error",
                    "message": "Group " + group_name + " existe deja",
                }
                return JsonResponse(message)
            serializer.save()
            data = serializer.data
            message = {
                "type": "success",
                "message": "Group " + data.get("Group_Name") + " ajouter avec succes",
                "id": data.get("Group_Id")
            }
            return JsonResponse(message)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GroupsInfo(APIView):
    def get(self, request, id):
        try:
            obj = Groups.objects.prefetch_related('Entity').filter(deleted_by__isnull=True).get(Group_Id=id)
            serializer = serializers.GroupsSerializer(obj)
            data = serializer.data
            return JsonResponse(data, safe=False)
        except Groups.DoesNotExist:
            message = {"message": "Group non trouver"}
            return JsonResponse(message, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id):
        try:
            obj = Groups.objects.filter(deleted_by__isnull=True).get(Group_Id=id)
            serializer = serializers.GroupsSerializer(obj, data=request.data)
            if serializer.is_valid():
                group_name = serializer.validated_data['Group_Name']
                if obj.Group_Name != request.data['Group_Name']:
                    if Groups.objects.filter(Group_Name=group_name).filter(deleted_by__isnull=True).exists():
                        message = {
                            "type": "error",
                            "message": "Group " + group_name + " existe deja",
                        }
                        return JsonResponse(message)
                serializer.save()
                data = serializer.data
                message = {
                    "type": "success",
                    "message": "Group " + data.get("Group_Name") + " modifier avec succes",
                    "id": data.get("Group_Id")
                }
                return JsonResponse(message)
        except Groups.DoesNotExist:
            message = {"message": "Group non trouver"}
            return JsonResponse(message, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, id):
        try:
            obj = Groups.objects.filter(deleted_by__isnull=True).get(Group_Id=id)
            serializer = serializers.GroupsSerializer(obj, data=request.data, partial=True)
            if serializer.is_valid():
                group_name = serializer.validated_data['Group_Name']
                if obj.Group_Name != request.data['Group_Name']:
                    if Groups.objects.filter(Group_Name=group_name).filter(deleted_by__isnull=True).exists():
                        message = {
                            "type": "error",
                            "message": "Group " + group_name + " existe deja",
                        }
                        return JsonResponse(message)
                serializer.save()
                data = serializer.data
                message = {
                    "type": "success",
                    "message": "Group " + data.get("Group_Name") + " modifier avec succes",
                    "id": data.get("Group_Id")
                }
                return JsonResponse(message)
        except Groups.DoesNotExist:
            message = {"message": "Group not found"}
            return JsonResponse(message, status=status.HTTP_404_NOT_FOUND)

    @csrf_exempt
    def delete(self, request, id):
        try:
            obj = Groups.objects.filter(deleted_by__isnull=True).get(Group_Id=id)
            name = obj.Group_Name
            obj.deleted_at = timezone.now()
            obj.deleted_by = 1
            obj.save()
            message = {
                "type": "success",
                "message": "Group " + name + " Supprimer avec succes",
            }
            return JsonResponse(message)
        except Groups.DoesNotExist:
            message = {"message": "Group not found"}
            return JsonResponse(message, status=status.HTTP_404_NOT_FOUND)


# CRUD Users
class UsersDetail(APIView):
    def get(self, request):
        obj = Users.objects.filter(deleted_by__isnull=True)
        serializer = serializers.UsersSerializer(obj, many=True)
        data = serializer.data
        return JsonResponse(data, safe=False)

    def post(self, request):
        serializer = serializers.UsersSerializer(data=request.data)
        if serializer.is_valid():
            user_email = serializer.validated_data['User_Email']
            if Users.objects.filter(User_Email=user_email).filter(deleted_by__isnull=True).exists():
                message = {
                    "type": "error",
                    "message": "Email User " + user_email + " existe deja",
                }
                return JsonResponse(message)
            # Save the user instance to database
            user = serializer.save()
            data = serializer.data
            user_id = data.get("User_Id")

            user_permission_data = request.data.get("User_Permission")
            user_role_data = request.data.get("User_Role")
            if user_permission_data and user_role_data:
                # Add Permission
                if user_permission_data.get("add") is True:
                    permission_id = 1
                    permission = Permissions.objects.get(Id=permission_id)
                    Permission_User.objects.create(Permission=permission, User=user)
                # View Permission
                if user_permission_data.get("view") is True:
                    permission_id = 2
                    permission = Permissions.objects.get(Id=permission_id)
                    Permission_User.objects.create(Permission=permission, User=user)
                # Update Permission
                if user_permission_data.get("update") is True:
                    permission_id = 3
                    permission = Permissions.objects.get(Id=permission_id)
                    Permission_User.objects.create(Permission=permission, User=user)
                # Delete Permission
                if user_permission_data.get("delete") is True:
                    permission_id = 4
                    permission = Permissions.objects.get(Id=permission_id)
                    Permission_User.objects.create(Permission=permission, User=user)
                # Sms Permission
                if user_permission_data.get("sms") is True:
                    permission_id = 5
                    permission = Permissions.objects.get(Id=permission_id)
                    Permission_User.objects.create(Permission=permission, User=user)
                # Traceability Permission
                if user_permission_data.get("traceability") is True:
                    permission_id = 6
                    permission = Permissions.objects.get(Id=permission_id)
                    Permission_User.objects.create(Permission=permission, User=user)
                # Super Administrateur Roles
                if user_role_data == "Super Administrateur":
                    roles_id = [1, 2, 3]
                    for role_id in roles_id:
                        role = Roles.objects.get(Id=role_id)
                        Role_User.objects.create(Role=role, User=user)
                # Administrateur Roles
                if user_role_data == "Administrateur":
                    roles_id = [2, 3]
                    for role_id in roles_id:
                        role = Roles.objects.get(Id=role_id)
                        Role_User.objects.create(Role=role, User=user)
                # Member Roles
                if user_role_data == "Member":
                    role_id = 3
                    role = Roles.objects.get(Id=role_id)
                    Role_User.objects.create(Role=role, User=user)

            message = {
                "type": "success",
                "message": "User " + data.get("User_First_Name") + " ajouter avec succes",
                "id": user_id
            }

            return JsonResponse(message)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsersInfo(APIView):
    def get(self, request, id):
        try:
            obj = Users.objects.filter(deleted_by__isnull=True).get(User_Id=id)
            serializer = serializers.UsersSerializer(obj)
            data = serializer.data

            # Decode User_Password_Crypt and include it in the JSON response
            user_password_crypt = obj.User_Password_Crypt
            user_password_crypt_string = eval(user_password_crypt)
            decoded_password = base64.b85decode(user_password_crypt_string).decode("utf-8")
            data["Decoded_Password"] = decoded_password

            return JsonResponse(data, safe=False)
        except Users.DoesNotExist:
            message = {"message": "User non trouver"}
            return JsonResponse(message, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id):
        try:
            obj = Users.objects.get(User_Id=id)
            serializer = serializers.UsersSerializer(obj, data=request.data)
            if serializer.is_valid():
                user_email = serializer.validated_data['User_Email']
                if obj.User_Email != request.data['User_Email']:
                    if Users.objects.filter(User_Email=user_email).filter(deleted_by__isnull=True).exists():
                        message = {
                            "type": "error",
                            "message": "Email User " + user_email + " existe deja",
                        }
                        return JsonResponse(message)

                Permission_User.objects.filter(User=id).delete()
                Role_User.objects.filter(User=id).delete()
                user = serializer.save()
                data = serializer.data

                user_permission_data = request.data.get("User_Permission")
                user_role_data = request.data.get("User_Role")

                if user_permission_data and user_role_data:
                    # Add Permission
                    if user_permission_data.get("add") is True:
                        permission_id = 1
                        permission = Permissions.objects.get(Id=permission_id)
                        Permission_User.objects.create(Permission=permission, User=user)
                    # View Permission
                    if user_permission_data.get("view") is True:
                        permission_id = 2
                        permission = Permissions.objects.get(Id=permission_id)
                        Permission_User.objects.create(Permission=permission, User=user)
                    # Update Permission
                    if user_permission_data.get("update") is True:
                        permission_id = 3
                        permission = Permissions.objects.get(Id=permission_id)
                        Permission_User.objects.create(Permission=permission, User=user)
                    # Delete Permission
                    if user_permission_data.get("delete") is True:
                        permission_id = 4
                        permission = Permissions.objects.get(Id=permission_id)
                        Permission_User.objects.create(Permission=permission, User=user)
                    # Sms Permission
                    if user_permission_data.get("sms") is True:
                        permission_id = 5
                        permission = Permissions.objects.get(Id=permission_id)
                        Permission_User.objects.create(Permission=permission, User=user)
                    # Traceability Permission
                    if user_permission_data.get("traceability") is True:
                        permission_id = 6
                        permission = Permissions.objects.get(Id=permission_id)
                        Permission_User.objects.create(Permission=permission, User=user)
                    # Super Administrateur Roles
                    if user_role_data == "Super Administrateur":
                        roles_id = [1, 2, 3]
                        for role_id in roles_id:
                            role = Roles.objects.get(Id=role_id)
                            Role_User.objects.create(Role=role, User=user)
                    # Administrateur Roles
                    if user_role_data == "Administrateur":
                        roles_id = [2, 3]
                        for role_id in roles_id:
                            role = Roles.objects.get(Id=role_id)
                            Role_User.objects.create(Role=role, User=user)
                    # Member Roles
                    if user_role_data == "Member":
                        role_id = 3
                        role = Roles.objects.get(Id=role_id)
                        Role_User.objects.create(Role=role, User=user)

                message = {
                    "type": "success",
                    "message": "User " + data.get("User_First_Name") + " modifier avec succes",
                    "id": data.get("User_Id")
                }
                return JsonResponse(message)
        except Users.DoesNotExist:
            message = {"message": "User non trouver"}
            return JsonResponse(message, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, id):
        try:
            obj = Users.objects.get(User_Id=id)
            serializer = serializers.UsersSerializer(obj, data=request.data, partial=True)
            if serializer.is_valid():
                user_email = serializer.validated_data['User_Email']
                if Users.objects.filter(User_Email=user_email).filter(deleted_by__isnull=True).exists():
                    message = {
                        "type": "error",
                        "message": "Email User " + user_email + " existe deja",
                    }
                    return JsonResponse(message)
                Permission_User.objects.filter(User=id).delete()
                Role_User.objects.filter(User=id).delete()
                user = serializer.save()
                data = serializer.data

                user_permission_data = request.data.get("User_Permission")
                user_role_data = request.data.get("User_Role")

                if user_permission_data and user_role_data:
                    # Add Permission
                    if user_permission_data.get("add") is True:
                        permission_id = 1
                        permission = Permissions.objects.get(Id=permission_id)
                        Permission_User.objects.create(Permission=permission, User=user)
                    # View Permission
                    if user_permission_data.get("view") is True:
                        permission_id = 2
                        permission = Permissions.objects.get(Id=permission_id)
                        Permission_User.objects.create(Permission=permission, User=user)
                    # Update Permission
                    if user_permission_data.get("update") is True:
                        permission_id = 3
                        permission = Permissions.objects.get(Id=permission_id)
                        Permission_User.objects.create(Permission=permission, User=user)
                    # Delete Permission
                    if user_permission_data.get("delete") is True:
                        permission_id = 4
                        permission = Permissions.objects.get(Id=permission_id)
                        Permission_User.objects.create(Permission=permission, User=user)
                    # Sms Permission
                    if user_permission_data.get("sms") is True:
                        permission_id = 5
                        permission = Permissions.objects.get(Id=permission_id)
                        Permission_User.objects.create(Permission=permission, User=user)
                    # Traceability Permission
                    if user_permission_data.get("traceability") is True:
                        permission_id = 6
                        permission = Permissions.objects.get(Id=permission_id)
                        Permission_User.objects.create(Permission=permission, User=user)
                    # Super Administrateur Roles
                    if user_role_data == "Super Administrateur":
                        roles_id = [1, 2, 3]
                        for role_id in roles_id:
                            role = Roles.objects.get(Id=role_id)
                            Role_User.objects.create(Role=role, User=user)
                    # Administrateur Roles
                    if user_role_data == "Administrateur":
                        roles_id = [2, 3]
                        for role_id in roles_id:
                            role = Roles.objects.get(Id=role_id)
                            Role_User.objects.create(Role=role, User=user)
                    # Member Roles
                    if user_role_data == "Member":
                        role_id = 3
                        role = Roles.objects.get(Id=role_id)
                        Role_User.objects.create(Role=role, User=user)

                message = {
                    "type": "success",
                    "message": "User " + data.get("User_First_Name") + " modifier avec succes",
                    "id": data.get("User_Id")
                }
                return JsonResponse(message)
        except Users.DoesNotExist:
            message = {"message": "User non trouver"}
            return JsonResponse(message, status=status.HTTP_404_NOT_FOUND)

    @csrf_exempt
    def delete(self, request, id):
        try:
            obj = Users.objects.get(User_Id=id)
            name = obj.User_First_Name
            obj.deleted_at = timezone.now()
            obj.deleted_by = 1
            obj.save()
            message = {
                "type": "success",
                "message": "User " + name + " Supprimer avec succes",
            }
            return JsonResponse(message)
        except Users.DoesNotExist:
            message = {"message": "User non trouver"}
            return JsonResponse(message, status=status.HTTP_404_NOT_FOUND)


# CRUD NumberList
class NumberListDetail(APIView):
    def get(self, request):
        obj = Number_List.objects.filter(deleted_by__isnull=True)
        serializer = serializers.NumberListSerializer(obj, many=True)
        data = serializer.data
        return JsonResponse(data, safe=False)

    def post(self, request):
        serializer = serializers.NumberListSerializer(data=request.data)
        if serializer.is_valid():
            Number = serializer.validated_data['Number']
            if Number_List.objects.filter(Number=Number).filter(deleted_by__isnull=True).exists():
                message = {
                    "type": "error",
                    "message": "Numéro " + Number + " existe deja",
                }
                return JsonResponse(message)
            serializer.save()
            data = serializer.data
            message = {
                "type": "success",
                "message": "Numéro " + data.get("Number_Name") + " ajouter avec succes",
                "id": data.get("Number_Id")
            }
            return JsonResponse(message)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NumberListInfo(APIView):
    def get(self, request, id):
        try:
            obj = Number_List.objects.filter(deleted_by__isnull=True).get(Number_Id=id)
            serializer = serializers.NumberListSerializer(obj)
            data = serializer.data
            return JsonResponse(data, safe=False)
        except Number_List.DoesNotExist:
            message = {"message": "Number not found"}
            return JsonResponse(message, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id):
        try:
            obj = Number_List.objects.get(Number_Id=id)
            serializer = serializers.NumberListSerializer(obj, data=request.data)
            if serializer.is_valid():
                Number = serializer.validated_data['Number']
                if obj.Number != request.data['Number']:
                    if Number_List.objects.filter(Number=Number).filter(deleted_by__isnull=True).exists():
                        message = {
                            "type": "error",
                            "message": "Numéro " + Number + " existe deja",
                        }
                        return JsonResponse(message)
                serializer.save()
                data = serializer.data
                message = {
                    "type": "success",
                    "message": "Numéro " + data.get("Number_Name") + " ajouter avec succes",
                    "id": data.get("Number_Id")
                }
                return JsonResponse(message)
        except Number_List.DoesNotExist:
            message = {"message": "Number not found"}
            return JsonResponse(message, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, id):
        try:
            obj = Number_List.objects.get(Number_Id=id)
            serializer = serializers.NumberListSerializer(obj, data=request.data, partial=True)
            if serializer.is_valid():
                Number = serializer.validated_data['Number']
                if obj.Number != request.data['Number']:
                    if Number_List.objects.filter(Number=Number).filter(deleted_by__isnull=True).exists():
                        message = {
                            "type": "error",
                            "message": "Numéro " + Number + " existe deja",
                        }
                        return JsonResponse(message)
                serializer.save()
                data = serializer.data
                message = {
                    "type": "success",
                    "message": "Numéro " + data.get("Number_Name") + " ajouter avec succes",
                    "id": data.get("Number_Id")
                }
                return JsonResponse(message)
        except Number_List.DoesNotExist:
            message = {"message": "Number not found"}
            return JsonResponse(message, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        try:
            obj = Number_List.objects.get(Number_Id=id)
            name = obj.Number_Name
            obj.deleted_at = timezone.now()
            obj.deleted_by = 1
            obj.save()
            message = {
                "type": "success",
                "message": "Numero " + name + " Supprimer avec succes",
            }
            return JsonResponse(message)
        except Number_List.DoesNotExist:
            message = {"message": "Number not found"}
            return JsonResponse(message, status=status.HTTP_404_NOT_FOUND)


# CRUD Directory
class DirectoryDetail(APIView):
    def get(self, request):
        obj = Directory.objects.filter(deleted_by__isnull=True)
        serializer = serializers.DirectorySerializer(obj, many=True)
        data = serializer.data
        return JsonResponse(data, safe=False)

    def post(self, request):
        serializer = serializers.DirectorySerializer(data=request.data.get("directory"))
        if serializer.is_valid():
            directory_name = serializer.validated_data['Directory_Name']
            if Directory.objects.filter(Directory_Name=directory_name, deleted_by__isnull=True).exists():
                message = {
                    "type": "error",
                    "message": "Répertoire " + directory_name + " existe déjà",
                }
                return JsonResponse(message)
            serializer.save()
            data_directory = serializer.data

            directory_id = data_directory.get("Directory_Id")
            lists = request.data.get("numbers")
            for number in lists:
                ResultSet = {"Directory_Id": directory_id, "Number_Id": number}
                serializer2 = serializers.RelationDirectoryNumberSerializer(data=ResultSet)
                if serializer2.is_valid():
                    serializer2.save()
            message = {
                "type": "success",
                "message": "Répertoire " + data_directory.get("Directory_Name") + " ajouté avec succes",
                "id": data_directory.get("Directory_Id")
            }
            return JsonResponse(message)


class DirectoryInfo(APIView):
    def get(self, request, id):
        try:
            directory = Directory.objects.filter(deleted_by__isnull=True).get(Directory_Id=id)
            relation_numbers = Relation_Directory_Number.objects.filter(deleted_by__isnull=True, Directory=directory)
            serialized_numbers = []
            for number in relation_numbers:
                serialized_numbers.append(serializers.RelationDirectoryNumberSerializer(number).data.get("Number"))
            data = {
                "directory_data": serializers.DirectorySerializer(directory).data,
                "list_numbers": serialized_numbers
            }
            return JsonResponse(data)
        except Directory.DoesNotExist:
            message = {"message": "Directory non trouvé"}
            return JsonResponse(message, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id):
        try:
            directory = Directory.objects.filter(deleted_by__isnull=True).get(Directory_Id=id)
            relation_numbers = Relation_Directory_Number.objects.filter(deleted_by__isnull=True, Directory=directory)
            relation_numbers.delete()
            serializer = serializers.DirectorySerializer(directory, data=request.data.get("directory"))
            if serializer.is_valid():
                # Check if Directory_Name is unique
                directory_name = serializer.validated_data['Directory_Name']
                if directory.Directory_Name != request.data.get("directory")['Directory_Name']:
                    if Directory.objects.filter(Directory_Name=directory_name, deleted_by__isnull=True).exists():
                        message = {
                            "type": "error",
                            "message": "Répertoire " + directory_name + " existe déjà",
                        }
                        return JsonResponse(message)
                serializer.save()
                data_directory = serializer.data

                numbers = request.data.get("numbers")
                for number in numbers:
                    ResultSet = {"Directory_Id": id, "Number_Id": number}
                    serializer2 = serializers.RelationDirectoryNumberSerializer(data=ResultSet)
                    if serializer2.is_valid():
                        serializer2.save()
                message = {
                    "type": "success",
                    "message": "Répertoire " + data_directory.get("Directory_Name") + " modifié avec succès",
                    "id": data_directory.get("Directory_Id")
                }
                return JsonResponse(message)
        except Directory.DoesNotExist:
            message = {"message": "Directory non trouvé"}
            return JsonResponse(message, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, id):
        try:
            directory = Directory.objects.filter(deleted_by__isnull=True).get(Directory_Id=id)
            relation_numbers = Relation_Directory_Number.objects.filter(deleted_by__isnull=True, Directory=directory)
            relation_numbers.delete()
            serializer = serializers.DirectorySerializer(directory, data=request.data.get("directory"), partial=True)
            if serializer.is_valid():
                # Check if Directory_Name is unique
                directory_name = serializer.validated_data['Directory_Name']
                if directory.Directory_Name != request.data.get("directory")['Directory_Name']:
                    if Directory.objects.filter(Directory_Name=directory_name, deleted_by__isnull=True).exists():
                        message = {
                            "type": "error",
                            "message": "Répertoire " + directory_name + " existe déjà",
                        }
                        return JsonResponse(message)
                serializer.save()
                data_directory = serializer.data

                numbers = request.data.get("numbers")
                for number in numbers:
                    ResultSet = {"Directory_Id": id, "Number_Id": number}
                    serializer2 = serializers.RelationDirectoryNumberSerializer(data=ResultSet)
                    if serializer2.is_valid():
                        serializer2.save()
                message = {
                    "type": "success",
                    "message": "Répertoire " + data_directory.get("Directory_Name") + " modifié avec succès",
                    "id": data_directory.get("Directory_Id")
                }
                return JsonResponse(message)
        except Directory.DoesNotExist:
            message = {"message": "Directory non trouvé"}
            return JsonResponse(message, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        try:
            obj = Directory.objects.get(Directory_Id=id)
            obj.delete()
            name = obj.Directory_Name
            obj.deleted_at = timezone.now()
            obj.deleted_by = 1
            obj.save()
            message = {
                "type": "success",
                "message": "Répertoire " + name + " Supprimer avec succes",
            }
            return JsonResponse(message)
        except Directory.DoesNotExist:
            message = {"message": "Directory not found"}
            return JsonResponse(message, status=status.HTTP_404_NOT_FOUND)


# CRUD Message
class Mailing_ListDetail(APIView):
    def get(self, request):
        obj = Mailing_List.objects.filter(deleted_by__isnull=True)
        serializer = serializers.Mailing_ListSerializer(obj, many=True)
        data = serializer.data
        return JsonResponse(data, safe=False)

    def post(self, request):
        serializer = Mailing_ListSerializer(data=request.data)
        if serializer.is_valid():
            Mailing_List_Name = serializer.validated_data['Mailing_List_Name']
            if Mailing_List.objects.filter(Mailing_List_Name=Mailing_List_Name, deleted_by__isnull=True).exists():
                message = {
                    "type": "error",
                    "message": "Liste d'envoi " + Mailing_List_Name + " existe deja",
                }
                return JsonResponse(message)
            # Check the type of file (.csv)
            file = request.FILES.get('Mailing_List_Url')
            if file:
                ext = os.path.splitext(file.name)[1]
                if ext.lower() != '.csv':
                    message = {
                        "type": "warning",
                        "message": "Liste doit etre un fichier .csv"
                    }
                    return JsonResponse(message)
            serializer.save()
            # Return a JSON response with the file URL and a success message
            message = {
                "type": "success",
                "message": "Liste ajouter avec succes"
            }
            return JsonResponse(message, status=status.HTTP_201_CREATED)
        else:
            # Return a JSON response with an error message
            message = {
                'message': 'error',
                'errors': serializer.errors
            }
            return JsonResponse(message, status=status.HTTP_400_BAD_REQUEST)


class Mailing_ListInfo(APIView):
    def get(self, request, id):
        try:
            obj = Mailing_List.objects.filter(deleted_by__isnull=True).get(Mailing_List_Id=id)
            serializer = serializers.Mailing_ListSerializer(obj)
            data = serializer.data
            return JsonResponse(data, safe=False)
        except Mailing_List.DoesNotExist:
            message = {"message": "Liste non trouver"}
            return JsonResponse(message, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id):
        try:
            obj = Mailing_List.objects.get(Mailing_List_Id=id)
            serializer = serializers.Mailing_ListSerializer(obj, data=request.data)
            if serializer.is_valid():
                Mailing_List_Name = serializer.validated_data['Mailing_List_Name']
                if obj.Mailing_List_Name != request.data['Mailing_List_Name']:
                    if Mailing_List.objects.filter(Mailing_List_Name=Mailing_List_Name,
                                                   deleted_by__isnull=True).exclude(Mailing_List_Id=id).exists():
                        message = {
                            "type": "error",
                            "message": "Liste d'envoi " + Mailing_List_Name + " existe deja",
                        }
                        return JsonResponse(message)
                # Check the type of file (.csv)
                file = request.FILES.get('Mailing_List_Url')
                if file:
                    ext = os.path.splitext(file.name)[1]
                    if ext.lower() != '.csv':
                        message = {
                            "type": "warning",
                            "message": "Liste doit etre un fichier .csv"
                        }
                        return JsonResponse(message)
                serializer.save()
                # Return a JSON response with the file URL and a success message
                message = {
                    "type": "success",
                    "message": "Liste modifier avec succes"
                }
                return JsonResponse(message)
        except Mailing_List.DoesNotExist:
            message = {"message": "Liste d'envoi non trouver"}
            return JsonResponse(message, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, id):
        try:
            obj = Mailing_List.objects.get(Mailing_List_Id=id)
            serializer = serializers.Mailing_ListSerializer(obj, data=request.data, partial=True)
            if serializer.is_valid():
                # Check if Mailing_List_Name is unique
                Mailing_List_Name = serializer.validated_data.get('Mailing_List_Name')
                if obj.Mailing_List_Name != request.data['Mailing_List_Name']:
                    if Mailing_List.objects.filter(Mailing_List_Name=Mailing_List_Name,
                                                   deleted_by__isnull=True).exclude(Mailing_List_Id=id).exists():
                        message = {
                            "type": "error",
                            "message": "Liste d'envoi " + Mailing_List_Name + " existe deja",
                        }
                        return JsonResponse(message)
                # Check if Mailing_List_File is a .csv file
                file = request.FILES.get('Mailing_List_Url')
                if file:
                    ext = os.path.splitext(file.name)[1]
                    if ext.lower() != '.csv':
                        message = {
                            "type": "warning",
                            "message": "Liste doit etre un fichier .csv"
                        }
                        return JsonResponse(message)
                serializer.save()
                # Return a JSON response with a success message
                message = {
                    "type": "success",
                    "message": "Liste modifiée avec succès"
                }
                return JsonResponse(message)
        except Mailing_List.DoesNotExist:
            message = {"message": "Liste d'envoi non trouvée"}
            return JsonResponse(message, status=status.HTTP_404_NOT_FOUND)

    @csrf_exempt
    def delete(self, request, id):
        try:
            obj = Mailing_List.objects.get(Mailing_List_Id=id)
            name = obj.Mailing_List_Name
            obj.deleted_at = timezone.now()
            obj.deleted_by = 1
            obj.save()
            message = {
                "type": "success",
                "message": "Entite " + name + " Supprimer avec succes",
            }
            return JsonResponse(message)
        except Mailing_List.DoesNotExist:
            message = {"message": "Entity not found"}
            return JsonResponse(message, status=status.HTTP_404_NOT_FOUND)


# CRUD Message
class MessageDetail(APIView):
    def get(self, request):
        obj = Predefined_Message.objects.filter(deleted_by__isnull=True)
        serializer = serializers.Predefined_MessageSerializer(obj, many=True)
        data = serializer.data
        return JsonResponse(data, safe=False)

    def post(self, request):
        serializer = serializers.Predefined_MessageSerializer(data=request.data)
        if serializer.is_valid():
            Message_Name = serializer.validated_data['Message_Name']
            if Predefined_Message.objects.filter(Message_Name=Message_Name).filter(deleted_by__isnull=True).exists():
                message = {
                    "type": "error",
                    "message": "Nom Message " + Message_Name + " existe deja",
                }
                return JsonResponse(message)
            serializer.save()
            data = serializer.data
            message = {
                "type": "success",
                "message": "Message " + data.get("Message_Name") + " ajouter avec succes",
                "id": data.get("Message_Id")
            }
            return JsonResponse(message)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MessageInfo(APIView):
    def get(self, request, id):
        try:
            obj = Predefined_Message.objects.get(Message_Id=id)
            serializer = serializers.Predefined_MessageSerializer(obj)
            data = serializer.data
            return JsonResponse(data, safe=False)
        except Predefined_Message.DoesNotExist:
            message = {"message": "Message non trouver"}
            return JsonResponse(message, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id):
        try:
            obj = Predefined_Message.objects.get(Message_Id=id)
            serializer = serializers.Predefined_MessageSerializer(obj, data=request.data)
            if serializer.is_valid():
                Message_Name = serializer.validated_data['Message_Name']
                if obj.Message_Name != request.data['Message_Name']:
                    if Predefined_Message.objects.filter(Message_Name=Message_Name).filter(
                            deleted_by__isnull=True).exists():
                        message = {
                            "type": "error",
                            "message": "Nom Message " + Message_Name + " existe deja",
                        }
                        return JsonResponse(message)
                serializer.save()
                data = serializer.data
                message = {
                    "type": "success",
                    "message": "Message " + data.get("Message_Name") + " modifier avec succes",
                    "id": data.get("Message_Id")
                }
                return JsonResponse(message)
        except Predefined_Message.DoesNotExist:
            message = {"message": "Message not found"}
            return JsonResponse(message, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, id):
        try:
            obj = Predefined_Message.objects.get(Message_Id=id)
            serializer = serializers.Predefined_MessageSerializer(obj, data=request.data, partial=True)
            if serializer.is_valid():
                Message_Name = serializer.validated_data['Message_Name']
                if obj.Message_Name != request.data['Message_Name']:
                    if Predefined_Message.objects.filter(Message_Name=Message_Name).filter(
                            deleted_by__isnull=True).exists():
                        message = {
                            "type": "error",
                            "message": "Nom Message " + Message_Name + " existe deja",
                        }
                        return JsonResponse(message)
                serializer.save()
                data = serializer.data
                message = {
                    "type": "success",
                    "message": "Message " + data.get("Message_Name") + " modifier avec succes",
                    "id": data.get("Message_Id")
                }
                return JsonResponse(message)
        except Predefined_Message.DoesNotExist:
            message = {"message": "Message not found"}
            return JsonResponse(message, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        try:
            obj = Predefined_Message.objects.get(Message_Id=id)
            name = obj.Message_Name
            obj.deleted_at = timezone.now()
            obj.deleted_by = 1
            obj.save()
            message = {
                "type": "success",
                "message": "Message " + name + " Supprimer avec succes",
            }
            return JsonResponse(message)
        except Predefined_Message.DoesNotExist:
            message = {"message": "Message not found"}
            return JsonResponse(message, status=status.HTTP_404_NOT_FOUND)


# CRUD Traceability Message
class LogMessageDetail(APIView):
    def get(self, request):
        obj = Log_Message.objects.filter(deleted_by__isnull=True).order_by('created_at')
        serializer = serializers.Log_MessageSerializer(obj, many=True)
        data = serializer.data
        return JsonResponse(data, safe=False)


class LogMessageInfo(APIView):
    def get(self, request, id):
        try:
            obj = Log_Message.objects.get(Id=id)
            serializer = serializers.Log_MessageSerializer(obj)
            data = serializer.data
            return JsonResponse(data, safe=False)
        except Log_Message.DoesNotExist:
            message = {"message": "Message non trouver"}
            return JsonResponse(message, status=status.HTTP_404_NOT_FOUND)


# @csrf_exempt
class login(APIView):
    def post(self, request):
        email = request.data['Email']
        password = request.data['Password']

        obj = Users.objects.filter(deleted_by__isnull=True).filter(User_Email=email)
        # if user is not None
        if (obj.exists()):
            serializer = serializers.UsersSerializer(obj, many=True)
            user = serializer.data[0]
            # check_password
            if check_password(password, user.get("User_Password")):
                # Create a new User instance using the dictionary data
                username = User.objects.make_random_password(length=10)
                new_user = User(
                    username=username,
                    password=user.get('User_Password'),
                    email=user.get('User_Email'),
                    first_name=user.get('User_First_Name'),
                    last_name=user.get('User_Last_Name')
                )
                new_user.save()
                token = Token.objects.create(user=new_user)
                message = {
                    "type": "success",
                    "message": "Connexion réussie",
                    "token": token.key,
                    "user": user
                }
                return JsonResponse(message)
            else:
                message = {
                    "type": "warning",
                    "message": "Mot de passe incorrect",
                }
                return JsonResponse(message)
        else:
            message = {
                "type": "warning",
                "message": "E-mail incorrect",
            }
            return JsonResponse(message)


def logout(request):
    # Logout the user
    auth.logout(request)
    # Clear the user session
    request.session.clear()
    message = {
        "type": "success",
        "message": "Logout successful"
    }
    return JsonResponse(message)


# Get Modem  (Phone Info)
class Status(APIView):
    def get(self, request):
        # Execute the SQL query
        with connection.cursor() as cursor:
            query = """ SELECT * FROM smsdb.phones """
            cursor.execute(query)
            phone_info = cursor.fetchall()

        # Format the result as a list of dictionaries
        columns = [col[0] for col in cursor.description]
        phone_info = [dict(zip(columns, row)) for row in phone_info]

        # Return the phone information as JSON
        return JsonResponse(phone_info, safe=False)


# # Sending Normal Message with Gammu
# class Send_Normal_Sms(APIView):
#     def post(self, request):
#         Numbers_Liste = request.data['Numbers']
#         Message = request.data['Message']
#         User = request.data['User']
#         Date = request.data['Date']
#
#         config_files = [CONFIG_CONTENT_1, CONFIG_CONTENT_2, CONFIG_CONTENT_3]
#         total_configs = len(config_files)
#         config_index = 0
#
#         success_count = 0
#         failed_numbers = []
#         total_count = len(Numbers_Liste)
#
#         if not Date:
#             for number in Numbers_Liste:
#                 try:
#                     # Get the current configuration content
#                     config_content = config_files[config_index]
#
#                     # Create a temporary file for the configuration
#                     temp_config_file = tempfile.NamedTemporaryFile(delete=False)
#                     temp_config_file.write(config_content.encode())
#                     temp_config_file.close()
#
#                     # Create object for talking with phone
#                     state_machine = gammu.StateMachine()
#                     # Read the configuration from the given file
#                     state_machine.ReadConfig(Filename=temp_config_file.name)
#                     # Connect to the phone
#                     state_machine.Init()
#
#                     if len(Message) <= 160:
#                         message = {
#                             "Text": Message,
#                             "SMSC": {"Location": 1},
#                             "Number": number,
#                             "Coding": "Unicode_No_Compression"
#                         }
#                         result = state_machine.SendSMS(message)
#                     else:
#                         smsinfo = {
#                             "Class": -1,
#                             "Unicode": True,
#                             "Entries": [
#                                 {
#                                     "ID": "ConcatenatedTextLong",
#                                     "Buffer": Message
#                                 }
#                             ],
#                         }
#                         encoded = gammu.EncodeSMS(smsinfo)
#                         for message in encoded:
#                             message["SMSC"] = {"Location": 1}
#                             message["Number"] = number
#                             result = state_machine.SendSMS(message)
#
#                     if result:
#                         # Add log Message
#                         log_message = Log_Message(
#                             Recipient=number,
#                             Modem=str(config_index + 1),
#                             Type_Envoi="Sms Avec Numero",
#                             Status="Envoyer",
#                             Message=Message,
#                             User_id=User,
#                         )
#                         log_message.save()
#                         success_count += 1
#                     else:
#                         # Add log Message
#                         log_message = Log_Message(
#                             Recipient=number,
#                             Modem=str(config_index + 1),
#                             Type_Envoi="Sms Avec Numero",
#                             Status="Non Envoyer",
#                             Message=Message,
#                             User_id=User,
#                         )
#                         log_message.save()
#                         failed_numbers.append(number)
#
#                     state_machine.Terminate()
#                     # Delete the temporary configuration file
#                     os.remove(temp_config_file.name)
#
#                     # Move to the next configuration file
#                     config_index = (config_index + 1) % total_configs
#
#                 except Exception as e:
#                     failed_numbers.append(number)
#                     print(f"Failed to send SMS to number {number}: {str(e)}")
#
#             if success_count == total_count:
#                 message = {
#                     "type": "success",
#                     "message": "SMS envoyé à tous les numéros"
#                 }
#             else:
#                 message = {
#                     "type": "error",
#                     "message": "Échec de l'envoi de certains SMS",
#                     "failed_numbers": failed_numbers
#                 }
#
#             return JsonResponse(message)
#         else:
#             # Code to send message at the defined date
#             message = {
#                 "type": "success",
#                 "message": "SMS programmé"
#             }
#             return JsonResponse(message)
#
#
# # Sending Sms To Directories with Gammu
# class Send_Directories_Sms(APIView):
#     def post(self, request):
#         directory_id = request.data['Directory']
#         Message = request.data['Message']
#         User = request.data['User']
#         Date = request.data['Date']
#
#         config_files = [CONFIG_CONTENT_1, CONFIG_CONTENT_2, CONFIG_CONTENT_3]
#         total_configs = len(config_files)
#         config_index = 0
#
#         success_count = 0
#         failed_numbers = []
#         total_count = 0
#
#         # Get all numbers from the directory
#         directory = Directory.objects.filter(deleted_by__isnull=True).get(Directory_Id=directory_id)
#         relation_numbers = Relation_Directory_Number.objects.filter(deleted_by__isnull=True, Directory=directory)
#         serialized_numbers = []
#         for number in relation_numbers:
#             serialized_numbers.append(serializers.RelationDirectoryNumberSerializer(number).data["Number"])
#         numbers_list = [number["Number"] for number in serialized_numbers]
#         total_count = len(numbers_list)
#
#         if not Date:
#             for number in numbers_list:
#                 try:
#                     # Get the current configuration content
#                     config_content = config_files[config_index]
#
#                     # Create a temporary file for the configuration
#                     temp_config_file = tempfile.NamedTemporaryFile(delete=False)
#                     temp_config_file.write(config_content.encode())
#                     temp_config_file.close()
#
#                     # Create object for talking with phone
#                     state_machine = gammu.StateMachine()
#                     # Read the configuration from the given file
#                     state_machine.ReadConfig(Filename=temp_config_file.name)
#                     # Connect to the phone
#                     state_machine.Init()
#
#                     if len(Message) <= 160:
#                         message = {
#                             "Text": Message,
#                             "SMSC": {"Location": 1},
#                             "Number": number,
#                             "Coding": "Unicode_No_Compression"
#                         }
#                         result = state_machine.SendSMS(message)
#                     else:
#                         smsinfo = {
#                             "Class": -1,
#                             "Unicode": True,
#                             "Entries": [
#                                 {
#                                     "ID": "ConcatenatedTextLong",
#                                     "Buffer": Message
#                                 }
#                             ],
#                         }
#                         encoded = gammu.EncodeSMS(smsinfo)
#                         for message in encoded:
#                             message["SMSC"] = {"Location": 1}
#                             message["Number"] = number
#                             result = state_machine.SendSMS(message)
#
#                     if result:
#                         # Add log Message
#                         log_message = Log_Message(
#                             Recipient=number,
#                             Modem=str(config_index + 1),
#                             Type_Envoi="Sms Avec Repertoire",
#                             Status="Envoyer",
#                             Message=Message,
#                             User_id=User,
#                         )
#                         log_message.save()
#                         success_count += 1
#                     else:
#                         # Add log Message
#                         log_message = Log_Message(
#                             Recipient=number,
#                             Modem=str(config_index + 1),
#                             Type_Envoi="Sms Avec Repertoire",
#                             Status="Non Envoyer",
#                             Message=Message,
#                             User_id=User,
#                         )
#                         log_message.save()
#                         failed_numbers.append(number)
#
#                     state_machine.Terminate()
#                     # Delete the temporary configuration file
#                     os.remove(temp_config_file.name)
#
#                     # Move to the next configuration file
#                     config_index = (config_index + 1) % total_configs
#
#                 except Exception as e:
#                     failed_numbers.append(number)
#                     print(f"Failed to send SMS to number {number}: {str(e)}")
#
#             if success_count == total_count:
#                 message = {
#                     "type": "success",
#                     "message": "SMS envoyé à tous les numéros du répertoire"
#                 }
#             else:
#                 message = {
#                     "type": "error",
#                     "message": "Échec de l'envoi de certains SMS",
#                     "failed_numbers": failed_numbers
#                 }
#
#             return JsonResponse(message)
#         else:
#             # Code to send message at the defined date
#             message = {
#                 "type": "success",
#                 "message": "SMS programmé"
#             }
#             return JsonResponse(message)
#
#
# # Sending Sms To Mailing List with Gammu
# class Send_Mailing_List_Sms(APIView):
#     def post(self, request):
#         mailing_list_id = request.data['MailingList']
#         Message = request.data['Message']
#         User = request.data['User']
#         Date = request.data['Date']
#
#         config_files = [CONFIG_CONTENT_1, CONFIG_CONTENT_2, CONFIG_CONTENT_3]
#         total_configs = len(config_files)
#         config_index = 0
#
#         # Create a temporary file for the configuration
#         temp_config_file = tempfile.NamedTemporaryFile(delete=False)
#         temp_config_file.write(config_files[config_index].encode())
#         temp_config_file.close()
#
#         # Create object for talking with phone
#         state_machine = gammu.StateMachine()
#         # Read the configuration from the given file
#         state_machine.ReadConfig(Filename=temp_config_file.name)
#         # Connect to the phone
#         state_machine.Init()
#
#         # Get Mailing list object
#         mailing_list = Mailing_List.objects.filter(deleted_by__isnull=True).get(Mailing_List_Id=mailing_list_id)
#         # Access the path of the mailing list file
#         mailing_list_path = os.path.join(settings.MEDIA_ROOT, mailing_list.Mailing_List_Url.name)
#         mailing_list_data = []
#         failed_numbers = []
#
#         try:
#             with open(mailing_list_path, 'r', encoding='utf-8-sig') as file:
#                 csv_reader = csv.reader(file)
#                 first_row = next(csv_reader)
#
#                 # file csv have only list of number
#                 if len(first_row) == 1 and Message:
#                     for i, row in enumerate(csv_reader):
#                         if i == 0:
#                             # Remove the UTF-8 BOM from the first element of the first row
#                             phone_number = row[0].strip('""\ufeff')
#                         else:
#                             phone_number = row[0].strip('""')
#                         mailing_list_data.append(phone_number)
#
#                     Numbers = mailing_list_data
#                     success_count = 0
#                     total_count = len(Numbers)
#                     if not Date:
#                         for number in Numbers:
#                             try:
#                                 # Get the current configuration content
#                                 config_content = config_files[config_index]
#
#                                 # Create a temporary file for the configuration
#                                 temp_config_file = tempfile.NamedTemporaryFile(delete=False)
#                                 temp_config_file.write(config_content.encode())
#                                 temp_config_file.close()
#
#                                 # Create object for talking with phone
#                                 state_machine = gammu.StateMachine()
#                                 # Read the configuration from the given file
#                                 state_machine.ReadConfig(Filename=temp_config_file.name)
#                                 # Connect to the phone
#                                 state_machine.Init()
#
#                                 # Send a normal message if the message length is less than or equal to 160 characters
#                                 if len(Message) <= 160:
#                                     message = {
#                                         "Text": Message,
#                                         "SMSC": {"Location": 1},
#                                         "Number": number,
#                                         "Coding": "Unicode_No_Compression"
#                                     }
#                                     # Actually send the message
#                                     result = state_machine.SendSMS(message)
#                                 else:
#                                     # Create SMS info structure
#                                     smsinfo = {
#                                         "Class": -1,
#                                         "Unicode": True,
#                                         "Entries": [
#                                             {
#                                                 "ID": "ConcatenatedTextLong",
#                                                 "Buffer": Message
#                                             }
#                                         ],
#                                     }
#                                     # Encode messages
#                                     encoded = gammu.EncodeSMS(smsinfo)
#                                     # Send messages
#                                     for message in encoded:
#                                         # Fill in numbers
#                                         message["SMSC"] = {"Location": 1}
#                                         message["Number"] = number
#                                         # Actually send the message
#                                         result = state_machine.SendSMS(message)
#
#                                 if result:
#                                     # Add log Message
#                                     log_message = Log_Message(
#                                         Recipient=number,
#                                         Modem=str(config_index + 1),
#                                         Type_Envoi="Sms Avec Liste D'envoi",
#                                         Status="Envoyer",
#                                         Message=Message,
#                                         User_id=User,
#                                     )
#                                     log_message.save()
#                                     success_count += 1
#                                 else:
#                                     # Add log Message
#                                     log_message = Log_Message(
#                                         Recipient=number,
#                                         Modem=str(config_index + 1),
#                                         Type_Envoi="Sms Avec Liste D'envoi",
#                                         Status="Non Envoyer",
#                                         Message=Message,
#                                         User_id=User,
#                                     )
#                                     log_message.save()
#                                     failed_numbers.append(number)
#
#                             finally:
#                                 state_machine.Terminate()
#                                 # Delete the temporary configuration file
#                                 os.remove(temp_config_file.name)
#
#                             # Move to the next configuration file
#                             config_index = (config_index + 1) % total_configs
#
#                         if success_count == total_count:
#                             message = {
#                                 "type": "success",
#                                 "message": "SMS envoyé à tous les numéros du répertoire"
#                             }
#                         else:
#                             message = {
#                                 "type": "error",
#                                 "message": "Échec de l'envoi de certains SMS",
#                                 "failed_numbers": failed_numbers
#                             }
#
#                         return JsonResponse(message)
#
#                     else:
#                         # Code to send message at the defined date
#                         message = {
#                             "type": "success",
#                             "message": "Sms Programmé"
#                         }
#                         return JsonResponse(message)
#
#                 elif len(first_row) == 2 and not Message:
#                     for row in csv_reader:
#                         phone_number = row[0].strip('""')
#                         message = row[1].strip('""')
#                         mailing_list_data.append({'Phone_Number': phone_number, 'Message': message})
#
#                     file_data = mailing_list_data
#
#                     if not Date:
#                         success_count = 0
#                         total_count = len(file_data)
#                         for item in file_data:
#                             phone_number = item['Phone_Number']
#                             message_l = item['Message']
#
#                             try:
#                                 # Get the current configuration content
#                                 config_content = config_files[config_index]
#
#                                 # Create a temporary file for the configuration
#                                 temp_config_file = tempfile.NamedTemporaryFile(delete=False)
#                                 temp_config_file.write(config_content.encode())
#                                 temp_config_file.close()
#
#                                 # Create object for talking with phone
#                                 state_machine = gammu.StateMachine()
#                                 # Read the configuration from the given file
#                                 state_machine.ReadConfig(Filename=temp_config_file.name)
#                                 # Connect to the phone
#                                 state_machine.Init()
#
#                                 if len(message_l) <= 160:
#                                     message_data = {
#                                         "Text": message_l,
#                                         "SMSC": {"Location": 1},
#                                         "Number": phone_number,
#                                         "Coding": "Unicode_No_Compression"
#                                     }
#                                     # Actually send the message
#                                     result = state_machine.SendSMS(message_data)
#                                 else:
#                                     # Create SMS info structure
#                                     smsinfo = {
#                                         "Class": -1,
#                                         "Unicode": True,
#                                         "Entries": [
#                                             {
#                                                 "ID": "ConcatenatedTextLong",
#                                                 "Buffer": message_l
#                                             }
#                                         ],
#                                     }
#                                     # Encode messages
#                                     encoded = gammu.EncodeSMS(smsinfo)
#                                     # Send messages
#                                     for message in encoded:
#                                         # Fill in numbers
#                                         message["SMSC"] = {"Location": 1}
#                                         message["Number"] = phone_number
#                                         # Actually send the message
#                                         result = state_machine.SendSMS(message)
#
#                                 if result:
#                                     # Add log Message
#                                     log_message = Log_Message(
#                                         Recipient=phone_number,
#                                         Modem=str(config_index + 1),
#                                         Type_Envoi="Sms Avec Liste D'envoi",
#                                         Status="Envoyer",
#                                         Message=message_l,
#                                         User_id=User,
#                                     )
#                                     log_message.save()
#                                     success_count += 1
#                                 else:
#                                     # Add log Message
#                                     log_message = Log_Message(
#                                         Recipient=phone_number,
#                                         Modem=str(config_index + 1),
#                                         Type_Envoi="Sms Avec Liste D'envoi",
#                                         Status="Non Envoyer",
#                                         Message=message_l,
#                                         User_id=User,
#                                     )
#                                     log_message.save()
#                                     failed_numbers.append(phone_number)
#
#                             finally:
#                                 state_machine.Terminate()
#                                 # Delete the temporary configuration file
#                                 os.remove(temp_config_file.name)
#
#                             # Move to the next configuration file
#                             config_index = (config_index + 1) % total_configs
#
#                         if success_count == total_count:
#                             message = {
#                                 "type": "success",
#                                 "message": "SMS envoyé à tous les numéros"
#                             }
#                         else:
#                             message = {
#                                 "type": "error",
#                                 "message": "Échec de l'envoi de certains SMS",
#                                 "failed_numbers": failed_numbers
#                             }
#
#                         return JsonResponse(message)
#                     else:
#                         # Code to send message at the defined date
#                         message = {
#                             "type": "success",
#                             "message": "Sms Programmé"
#                         }
#                         return JsonResponse(message)
#
#         except FileNotFoundError:
#             return JsonResponse({'error': 'Mailing list file not found'})
#
#         except Exception as e:
#             return JsonResponse({'error': str(e)})
#
#
# # Sending Sms Link
# @csrf_exempt
# def Send_Link_Sms(request, email, password, numbers, message):
#     obj = Users.objects.filter(deleted_by__isnull=True).filter(User_Email=email)
#
#     # Check if user exists
#     if obj.exists():
#         serializer = serializers.UsersSerializer(obj, many=True)
#         user = serializer.data[0]
#
#         # Verify password
#         if check_password(password, user.get("User_Password")):
#             try:
#                 config_files = [CONFIG_CONTENT_1, CONFIG_CONTENT_2, CONFIG_CONTENT_3]
#                 total_configs = len(config_files)
#                 config_index = 0
#
#                 response = {
#                     "type": "success",
#                     "message": "SMS envoyé"
#                 }
#
#                 number_list = ast.literal_eval(numbers)  # Split the comma-separated numbers into a list
#
#                 for number in number_list:
#                     try:
#                         # Get the current configuration content
#                         config_content = config_files[config_index]
#
#                         # Create a temporary file for the configuration
#                         temp_config_file = tempfile.NamedTemporaryFile(delete=False)
#                         temp_config_file.write(config_content.encode())
#                         temp_config_file.close()
#
#                         # Create object for talking with phone
#                         state_machine = gammu.StateMachine()
#                         # Read the configuration from the given file
#                         state_machine.ReadConfig(Filename=temp_config_file.name)
#                         # Connect to the phone
#                         state_machine.Init()
#
#                         if len(message) <= 160:
#                             sms = {
#                                 "Text": message,
#                                 "SMSC": {"Location": 1},
#                                 "Number": number,
#                                 "Coding": "Unicode_No_Compression"
#                             }
#                             result = state_machine.SendSMS(sms)
#                         else:
#                             smsinfo = {
#                                 "Class": -1,
#                                 "Unicode": True,
#                                 "Entries": [
#                                     {
#                                         "ID": "ConcatenatedTextLong",
#                                         "Buffer": message
#                                     }
#                                 ],
#                             }
#                             encoded = gammu.EncodeSMS(smsinfo)
#                             for msg in encoded:
#                                 msg["SMSC"] = {"Location": 1}
#                                 msg["Number"] = number
#                                 result = state_machine.SendSMS(msg)
#                         if result:
#                             # Add log message
#                             log_message = Log_Message(
#                                 Recipient=number,
#                                 Modem=str(config_index + 1),
#                                 Type_Envoi="Link Sms",
#                                 Status="Envoyer",
#                                 Message=message,
#                                 User_id=user.get('User_Id'),  # Use the User_Id from the User object
#                             )
#                             log_message.save()
#                         else:
#                             # Add log message
#                             log_message = Log_Message(
#                                 Recipient=number,
#                                 Modem=str(config_index + 1),
#                                 Type_Envoi="Link Sms",
#                                 Status="Non Envoyer",
#                                 Message=message,
#                                 User_id=user.get('User_Id'),  # Use the User_Id from the User object
#                             )
#                             log_message.save()
#                             response = {
#                                 "type": "error",
#                                 "message": "Message non envoyé pour le numéro " + number,
#                             }
#                             break
#
#                         state_machine.Terminate()
#                         # Delete the temporary configuration file
#                         os.remove(temp_config_file.name)
#
#                         # Move to the next configuration file
#                         config_index = (config_index + 1) % total_configs
#
#                     except Exception as e:
#                     # Add log message
#                         log_message = Log_Message(
#                             Recipient=number,
#                             Modem=str(config_index + 1),
#                             Type_Envoi="Link Sms",
#                             Status="Non Envoyer",
#                             Message=message,
#                             User_id=user.get('User_Id'),  # Use the User_Id from the User object
#                         )
#                         log_message.save()
#                         response = {
#                             "type": "error",
#                             "message": "Message non envoyé",
#                         }
#                         return JsonResponse(response)
#
#                 return JsonResponse(response)
#
#             except Exception as e:
#                 response = {
#                     "type": "error",
#                     "message": "Une erreur s'est produite lors de l'envoi du SMS",
#                 }
#                 return JsonResponse(response)
#
#         else:
#             response = {
#                 "type": "warning",
#                 "message": "Mot de passe incorrect",
#             }
#             return JsonResponse(response)
#     else:
#         response = {
#             "type": "warning",
#             "message": "Email incorrect",
#         }
#         return JsonResponse(response)
#
# # Sending Sms Email
# @csrf_exempt
# def Send_Email_Sms(request, email, password, numbers, message):
#     obj = Users.objects.filter(deleted_by__isnull=True).filter(User_Email=email)
#
#     # Check if user exists
#     if obj.exists():
#         serializer = serializers.UsersSerializer(obj, many=True)
#         user = serializer.data[0]
#
#         # Verify password
#         if check_password(password, user.get("User_Password")):
#             try:
#                 config_files = [CONFIG_CONTENT_1, CONFIG_CONTENT_2, CONFIG_CONTENT_3]
#                 total_configs = len(config_files)
#                 config_index = 0
#
#                 response = {
#                     "type": "success",
#                     "message": "SMS envoyé"
#                 }
#
#                 number_list = ast.literal_eval(numbers)  # Split the comma-separated numbers into a list
#
#                 for number in number_list:
#                     try:
#                         # Get the current configuration content
#                         config_content = config_files[config_index]
#
#                         # Create a temporary file for the configuration
#                         temp_config_file = tempfile.NamedTemporaryFile(delete=False)
#                         temp_config_file.write(config_content.encode())
#                         temp_config_file.close()
#
#                         # Create object for talking with phone
#                         state_machine = gammu.StateMachine()
#                         # Read the configuration from the given file
#                         state_machine.ReadConfig(Filename=temp_config_file.name)
#                         # Connect to the phone
#                         state_machine.Init()
#
#                         if len(message) <= 160:
#                             sms = {
#                                 "Text": message,
#                                 "SMSC": {"Location": 1},
#                                 "Number": number,
#                                 "Coding": "Unicode_No_Compression"
#                             }
#                             result = state_machine.SendSMS(sms)
#                         else:
#                             smsinfo = {
#                                 "Class": -1,
#                                 "Unicode": True,
#                                 "Entries": [
#                                     {
#                                         "ID": "ConcatenatedTextLong",
#                                         "Buffer": message
#                                     }
#                                 ],
#                             }
#                             encoded = gammu.EncodeSMS(smsinfo)
#                             for msg in encoded:
#                                 msg["SMSC"] = {"Location": 1}
#                                 msg["Number"] = number
#                                 result = state_machine.SendSMS(msg)
#                         if result:
#                             # Add log message
#                             log_message = Log_Message(
#                                 Recipient=number,
#                                 Modem=str(config_index + 1),
#                                 Type_Envoi="Email Sms",
#                                 Status="Envoyer",
#                                 Message=message,
#                                 User_id=user.get('User_Id'),  # Use the User_Id from the User object
#                             )
#                             log_message.save()
#                         else:
#                             # Add log message
#                             log_message = Log_Message(
#                                 Recipient=number,
#                                 Modem=str(config_index + 1),
#                                 Type_Envoi="Email Sms",
#                                 Status="Non Envoyer",
#                                 Message=message,
#                                 User_id=user.get('User_Id'),  # Use the User_Id from the User object
#                             )
#                             log_message.save()
#                             response = {
#                                 "type": "error",
#                                 "message": "Message non envoyé pour le numéro " + number,
#                             }
#                             break
#
#                         state_machine.Terminate()
#                         # Delete the temporary configuration file
#                         os.remove(temp_config_file.name)
#
#                         # Move to the next configuration file
#                         config_index = (config_index + 1) % total_configs
#
#                     except Exception as e:
#                     # Add log message
#                         log_message = Log_Message(
#                             Recipient=number,
#                             Modem=str(config_index + 1),
#                             Type_Envoi="Email Sms",
#                             Status="Non Envoyer",
#                             Message=message,
#                             User_id=user.get('User_Id'),  # Use the User_Id from the User object
#                         )
#                         log_message.save()
#                         response = {
#                             "type": "error",
#                             "message": "Message non envoyé",
#                         }
#                         return JsonResponse(response)
#
#                 return JsonResponse(response)
#
#             except Exception as e:
#                 response = {
#                     "type": "error",
#                     "message": "Une erreur s'est produite lors de l'envoi du SMS",
#                 }
#                 return JsonResponse(response)
#
#         else:
#             response = {
#                 "type": "warning",
#                 "message": "Mot de passe incorrect",
#             }
#             return JsonResponse(response)
#     else:
#         response = {
#             "type": "warning",
#             "message": "Email incorrect",
#         }
#         return JsonResponse(response)
#
# # Sending Sms Monitoring
# @csrf_exempt
# def Send_Monitoring_Sms(request, email, password, numbers, message):
#     obj = Monitoring.objects.filter(deleted_by__isnull=True).filter(Monitoring_Email=email)
#
#     # Check if user exists
#     if obj.exists():
#         serializer = serializers.MonitoringSerializer(obj, many=True)
#         monitoring = serializer.data[0]
#
#         # Verify password
#         if check_password(password, monitoring.get("Monitoring_Password")):
#             try:
#                 config_files = [CONFIG_CONTENT_1, CONFIG_CONTENT_2, CONFIG_CONTENT_3]
#                 total_configs = len(config_files)
#                 config_index = 0
#
#                 response = {
#                     "type": "success",
#                     "message": "SMS envoyé"
#                 }
#
#                 number_list = ast.literal_eval(numbers)  # Split the comma-separated numbers into a list
#
#                 for number in number_list:
#                     try:
#                         # Get the current configuration content
#                         config_content = config_files[config_index]
#
#                         # Create a temporary file for the configuration
#                         temp_config_file = tempfile.NamedTemporaryFile(delete=False)
#                         temp_config_file.write(config_content.encode())
#                         temp_config_file.close()
#
#                         # Create object for talking with phone
#                         state_machine = gammu.StateMachine()
#                         # Read the configuration from the given file
#                         state_machine.ReadConfig(Filename=temp_config_file.name)
#                         # Connect to the phone
#                         state_machine.Init()
#
#                         if len(message) <= 160:
#                             sms = {
#                                 "Text": message,
#                                 "SMSC": {"Location": 1},
#                                 "Number": number,
#                                 "Coding": "Unicode_No_Compression"
#                             }
#                             result = state_machine.SendSMS(sms)
#                         else:
#                             smsinfo = {
#                                 "Class": -1,
#                                 "Unicode": True,
#                                 "Entries": [
#                                     {
#                                         "ID": "ConcatenatedTextLong",
#                                         "Buffer": message
#                                     }
#                                 ],
#                             }
#                             encoded = gammu.EncodeSMS(smsinfo)
#                             for msg in encoded:
#                                 msg["SMSC"] = {"Location": 1}
#                                 msg["Number"] = number
#                                 result = state_machine.SendSMS(msg)
#                         if result:
#                             # Add log message
#                             log_message = Log_Message(
#                                 Recipient=number,
#                                 Modem=str(config_index + 1),
#                                 Type_Envoi="Email Sms",
#                                 Status="Envoyer",
#                                 Message=message,
#                                 User_id=monitoring.get('Monitoring_Id'),
#                             )
#                             log_message.save()
#                         else:
#                             # Add log message
#                             log_message = Log_Message(
#                                 Recipient=number,
#                                 Modem=str(config_index + 1),
#                                 Type_Envoi="Email Sms",
#                                 Status="Non Envoyer",
#                                 Message=message,
#                                 User_id=monitoring.get('Monitoring_Id'),
#                             )
#                             log_message.save()
#                             response = {
#                                 "type": "error",
#                                 "message": "Message non envoyé pour le numéro " + number,
#                             }
#                             break
#
#                         state_machine.Terminate()
#                         # Delete the temporary configuration file
#                         os.remove(temp_config_file.name)
#
#                         # Move to the next configuration file
#                         config_index = (config_index + 1) % total_configs
#
#                     except Exception as e:
#                     # Add log message
#                         log_message = Log_Message(
#                             Recipient=number,
#                             Modem=str(config_index + 1),
#                             Type_Envoi="Email Sms",
#                             Status="Non Envoyer",
#                             Message=message,
#                             User_id=monitoring.get('Monitoring_Id'),
#                         )
#                         log_message.save()
#                         response = {
#                             "type": "error",
#                             "message": "Message non envoyé",
#                         }
#                         return JsonResponse(response)
#
#                 return JsonResponse(response)
#
#             except Exception as e:
#                 response = {
#                     "type": "error",
#                     "message": "Une erreur s'est produite lors de l'envoi du SMS",
#                 }
#                 return JsonResponse(response)
#
#         else:
#             response = {
#                 "type": "warning",
#                 "message": "Mot de passe incorrect",
#             }
#             return JsonResponse(response)
#     else:
#         response = {
#             "type": "warning",
#             "message": "Email incorrect",
#         }
#         return JsonResponse(response)

class EmailToSms(APIView):
    def get(self, request):
        obj = Email_To_Sms.objects
        serializer = serializers.Email_To_SmsSerializer(obj, many=True)
        data = serializer.data[0]
        # Convert String to List
        data["Recipient"] = ast.literal_eval(data.get("Recipient"))
        return JsonResponse(data, safe=False)

    def post(self, request):
        # Variable for Configuration Server
        client = request.data['Client']
        host_name = request.data['HostName']
        email_server = request.data['Email_Server']
        password_server = request.data['Password_Server']
        port = request.data['Port']

        # Variable for Configuration User
        email_user = request.data['Email_User']
        password_user = request.data['Password_User']
        recipient = request.data['Recipient']
        reload_time = request.data['Reload_Time']

        response_data = {}
        try:
            # Clear the Email_To_Sms table
            Email_To_Sms.objects.all().delete()

            if client == "imap":
                # Execute the script for IMAP
                script_path = "/home/mysms/backend/addon/mail_to_sms/myimaplib.py"
                command = f"python {script_path} {host_name} {port} {email_server} {password_server} {email_user} {password_user} {recipient} {reload_time}"

                # Schedule the cron job
                cron = CronTab(user='apache')  # Replace 'your_username' with your username
                job = cron.new(command=command)
                job.minute.every(int(reload_time))  # Schedule job to run every 'reload_time' minutes
                cron.write()

                email_to_sms = Email_To_Sms(
                    Client=client,
                    HostName=host_name,
                    Email_Server=email_server,
                    Password_Server=password_server,
                    Port=port,
                    Recipient=recipient,
                    Email_User=email_user,
                    Password_User=password_user,
                    Reload_Time=reload_time
                )
                email_to_sms.save()

                response_data["type"] = "success"
                response_data["message"] = "Scripts IMAP a été exécuté avec succès."
            elif client == "pop3":
                # Execute the script for POP3
                script_path = "/home/mysms/backend/addon/mail_to_sms/mypoplib.py"
                command = f"python {script_path} {host_name} {port} {email_server} {password_server} {email_user} {password_user} {recipient} {reload_time}"

                # Schedule the cron job
                cron = CronTab(user='apache')  # Replace 'your_username' with your username
                job = cron.new(command=command)
                job.minute.every(int(reload_time))  # Schedule job to run every 'reload_time' minutes
                cron.write()

                email_to_sms = Email_To_Sms(
                    Client=client,
                    HostName=host_name,
                    Email_Server=email_server,
                    Password_Server=password_server,
                    Port=port,
                    Recipient=recipient,
                    Email_User=email_user,
                    Password_User=password_user,
                    Reload_Time=reload_time
                )
                email_to_sms.save()

                response_data["type"] = "success"
                response_data["message"] = "Scripts POP3 a été exécuté avec succès."
            else:
                # Execute the script for OWA
                script_path = "/home/mysms/backend/addon/mail_to_sms/myowalib.py"
                command = f"python {script_path} {host_name} {port} {email_server} {password_server} {email_user} {password_user} {recipient} {reload_time}"

                # Schedule the cron job
                cron = CronTab(user='apache')  # Replace 'your_username' with your username
                job = cron.new(command=command)
                job.minute.every(int(reload_time))  # Schedule job to run every 'reload_time' minutes
                cron.write()

                email_to_sms = Email_To_Sms(
                    Client=client,
                    HostName=host_name,
                    Email_Server=email_server,
                    Password_Server=password_server,
                    Port=port,
                    Recipient=recipient,
                    Email_User=email_user,
                    Password_User=password_user,
                    Reload_Time=reload_time
                )
                email_to_sms.save()

                response_data["type"] = "success"
                response_data["message"] = "Scripts OWA a été exécuté avec succès."

        except Exception as e:
            response_data["type"] = "error"
            response_data["message"] = str(e)

        return JsonResponse(response_data)


# Send Back Sms Not Send
class SmsNotSendDetail(APIView):
    def get(self, request):
        obj = Log_Message.objects.filter(Status="Non Envoyer", Send_Back__isnull=True)
        serializer = Log_MessageSerializer(obj, many=True)
        data = serializer.data
        return JsonResponse(data, safe=False)

    # def post(self, request):
    #     Number = request.data["Number"]
    #     Message = request.data["Message"]
    #     User = request.data["User"]
    #     Sms = request.data["Sms"]
    #
    #     obj = Log_Message.objects.filter(Status="Non Envoyer", Send_Back__isnull=True).get(Id=Sms)
    #     obj.Send_Back = 'True'  # Set Send_Back to False
    #     serializer = Log_MessageSerializer(obj, data=request.data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #
    #     config_files = [CONFIG_CONTENT_1, CONFIG_CONTENT_2, CONFIG_CONTENT_3]
    #     total_configs = len(config_files)
    #     config_index = 0
    #
    #     try:
    #         # Get the current configuration content
    #         config_content = config_files[config_index]
    #
    #         # Create a temporary file for the configuration
    #         temp_config_file = tempfile.NamedTemporaryFile(delete=False)
    #         temp_config_file.write(config_content.encode())
    #         temp_config_file.close()
    #
    #         # Create object for talking with the phone
    #         state_machine = gammu.StateMachine()
    #
    #         # Read the configuration from the given file
    #         state_machine.ReadConfig(Filename=temp_config_file.name)
    #
    #         # Connect to the phone
    #         state_machine.Init()
    #
    #         if len(Message) <= 160:
    #             sms = {
    #                 "Text": Message,
    #                 "SMSC": {"Location": 1},
    #                 "Number": Number,
    #                 "Coding": "Unicode_No_Compression"
    #             }
    #             result = state_machine.SendSMS(sms)
    #         else:
    #             smsinfo = {
    #                 "Class": -1,
    #                 "Unicode": True,
    #                 "Entries": [
    #                     {
    #                         "ID": "ConcatenatedTextLong",
    #                         "Buffer": Message
    #                     }
    #                 ],
    #             }
    #             encoded = gammu.EncodeSMS(smsinfo)
    #             for msg in encoded:
    #                 msg["SMSC"] = {"Location": 1}
    #                 msg["Number"] = Number
    #                 result = state_machine.SendSMS(msg)
    #
    #         if result:
    #             # Add log message
    #             log_message = Log_Message(
    #                 Recipient=Number,
    #                 Modem=str(config_index + 1),
    #                 Type_Envoi="Sms Renvoyer",
    #                 Status="Envoyer",
    #                 Message=Message,
    #                 User_id=User
    #             )
    #             log_message.save()
    #             response = {
    #                 "type": "success",
    #                 "message": "Message envoyé pour le numéro " + Number,
    #             }
    #         else:
    #             # Add log message
    #             log_message = Log_Message(
    #                 Recipient=Number,
    #                 Modem=str(config_index + 1),
    #                 Type_Envoi="Sms Renvoyer",
    #                 Status="Non Envoyer",
    #                 Message=Message,
    #                 User_id=User
    #             )
    #             log_message.save()
    #             response = {
    #                 "type": "error",
    #                 "message": "Message non envoyé pour le numéro " + Number,
    #             }
    #
    #         state_machine.Terminate()
    #         # Delete the temporary configuration file
    #         os.remove(temp_config_file.name)
    #
    #         return JsonResponse(response)
    #
    #     except Exception as e:
    #         response = {
    #             "type": "error",
    #             "message":str(e),
    #         }
    #         return JsonResponse(response)


class SmsNotSendInfo(APIView):
    def patch(self, request, id):
        try:
            obj = Log_Message.objects.filter(Status="Non Envoyer", Send_Back__isnull=True).get(Id=id)
            obj.Send_Back = 'False'  # Set Send_Back to False
            serializer = Log_MessageSerializer(obj, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                message = {
                    "type": "success",
                    "message": "Message Ignorer Avec Succes"
                }
                return JsonResponse(message)
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Log_Message.DoesNotExist:
            message = {"message": "Message non trouver"}
            return JsonResponse(message, status=status.HTTP_404_NOT_FOUND)

# Permissions Users
class PermissionsUser(APIView):
    def get(self, request, id):
        try:
            obj = Permission_User.objects.filter(User=id)
            serializer = Permission_UserSerializer(obj, many=True)
            data = serializer.data
            List = []
            for item in data:
                List.append(item.get("Permission").get("Permission_Name"))

            def element_exists(lst, element):
                # Try to get the index of the element in the list
                try:
                    lst.index(element)
                    # If the element is found, return True
                    return True
                # If a ValueError is raised, the element is not in the list
                except ValueError:
                    # Return False in this case
                    return False

            Permissions = {
                "add": element_exists(List, "add"),
                "view": element_exists(List, "view"),
                "update": element_exists(List, "update"),
                "delete": element_exists(List, "delete"),
                "sms": element_exists(List, "sms"),
                "traceability": element_exists(List, "traceability"),
            }
            return JsonResponse(Permissions, safe=False)
        except Permission_User.DoesNotExist:
            message = {"message": "Permission User non trouver"}
            return JsonResponse(message, status=status.HTTP_404_NOT_FOUND)

# Role Users
class RoleUser(APIView):
    def get(self, request, id):
        try:
            obj = Role_User.objects.filter(User=id)
            serializer = Role_UserSerializer(obj, many=True)
            data = serializer.data
            List = []
            for item in data:
                List.append(item.get("Role").get("Role_Name"))

            def element_exists(lst, element):
                # Try to get the index of the element in the list
                try:
                    lst.index(element)
                    # If the element is found, return True
                    return True
                # If a ValueError is raised, the element is not in the list
                except ValueError:
                    # Return False in this case
                    return False

            Roles = {
                "Super_Administrateur": element_exists(List, "Super Administrateur"),
                "Administrateur": element_exists(List, "Administrateur"),
                "Member": element_exists(List, "Member"),
            }
            return JsonResponse(Roles, safe=False)
        except Role_User.DoesNotExist:
            message = {"message": "Role User non trouver"}
            return JsonResponse(message, status=status.HTTP_404_NOT_FOUND)
