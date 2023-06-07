import os
import sys
import csv
import pytz
import time
# import gammu
import base64
import random
import tempfile
from . import serializers
from django.contrib import auth
from django.db import connection
from Project_SMS import settings
from rest_framework import status
from django.utils import timezone
from django.http import JsonResponse
from datetime import datetime, timedelta
from rest_framework.views import APIView
from django.shortcuts import render, redirect
from .serializers import Mailing_ListSerializer
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from .models import Entities, Groups, Users, Number_List, Directory, Predefined_Message, Mailing_List, \
    Relation_Directory_Number
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

#### Config Files ####


config_content_1 = """
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

# file_config_1="/var/www/html/modem-1"
# file_config_2="/root/modem-2"


#### End Config Files#############################################################################################################


def index(request):
    return render(request, 'index.html')


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
            obj = Groups.objects.objects.filter(deleted_by__isnull=True).get(Group_Id=id)
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
            obj = Groups.objects.objects.filter(deleted_by__isnull=True).get(Group_Id=id)
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
            obj = Groups.objects.objects.filter(deleted_by__isnull=True).get(Group_Id=id)
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
            serializer.save()
            data = serializer.data
            message = {
                "type": "success",
                "message": "User " + data.get("User_First_Name") + " ajouter avec succes",
                "id": data.get("User_Id")
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
                serializer.save()
                data = serializer.data
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
                serializer.save()
                data = serializer.data
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
            if Directory.objects.filter(Directory_Name=directory_name).filter(deleted_by__isnull=True).exists():
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
                if directory_name != request.data.get("directory").get("Directory_Name"):
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
                if directory_name != request.data.get("directory").get("Directory_Name"):
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


class Mailing_ListDetail(APIView):
    def get(self, request):
        obj = Mailing_List.objects.filter(deleted_by__isnull=True)
        serializer = serializers.Mailing_ListSerializer(obj, many=True)
        data = serializer.data
        return JsonResponse(data, safe=False)

    def post(self, request):
        serializer = Mailing_ListSerializer(data=request.data)
        if serializer.is_valid():
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
                file = request.FILES.get('Mailing_List_Url')
                if obj.Mailing_List_Name != request.data['Mailing_List_Name']:

                    if Mailing_List.objects.filter(Mailing_List_Name=Mailing_List_Name).filter(
                            deleted_by__isnull=True).exists():
                        message = {
                            "type": "error",
                            "message": "Liste d'envoi " + Mailing_List_Name + " existe deja",
                        }
                        return JsonResponse(message)
                # Check the type of file (.csv)
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
                mailing_list_name = serializer.validated_data.get('Mailing_List_Name')
                if Mailing_List.objects.filter(Mailing_List_Name=mailing_list_name).filter(
                        deleted_by__isnull=True).exclude(Mailing_List_Id=id).exists():
                    message = {"message": "Nom de la Liste existe deja"}
                    return JsonResponse(message, status=status.HTTP_400_BAD_REQUEST)

                # Check if Mailing_List_File is a .csv file
                mailing_list_file = request.FILES.get('Mailing_List_File')
                if mailing_list_file:
                    ext = os.path.splitext(mailing_list_file.name)[1]
                    if ext.lower() != '.csv':
                        message = {"message": "Mailing list file must be a .csv file."}
                        return JsonResponse(message, status=status.HTTP_400_BAD_REQUEST)

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
                    "message": "Login successful",
                    "token": token.key,
                    "user": user
                }
                return JsonResponse(message)
            else:
                message = {
                    "type": "warning",
                    "message": "Mot de passe Incorrect",
                }
                return JsonResponse(message)
        else:
            message = {
                "type": "warning",
                "message": "Email Incorrect",
            }
            return JsonResponse(message)

        # # Authenticate the user based on email and hashed password
        # user = Users.objects.filter(User_Email=email).filter(deleted_by__isnull=True)
        # data = {
        #     "email": email,
        #     "password": password
        # }
        # return JsonResponse(user)
        # if user is not None and check_password(password, user.User_Password):
        #     auth.login(request, user)
        #     # Save Object User in Session
        #     request.session['user'] = {
        #         # Add more fields as needed
        #         'id': user.User_Id,
        #         'email': user.User_Email,
        #         'first_name': user.User_First_Name,
        #         'last_name': user.User_Last_Name,
        #         'role': user.User_Role
        #     }
        #     token = Token.objects.create(user=user)
        #     message = {
        #         "type": "success",
        #         "message": "Login successful",
        #         "token": token.key
        #     }
        #     return JsonResponse(message)
        # else:
        #     message = {
        #         "type": "error",
        #         "message": "Email or mot de passe Incorrect",
        #     }
        #     return JsonResponse(message, status=401)


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


# Sending Normal Message with Gammu
class Send_Normal_Sms(APIView):
    def post(self, request):
        Numbers_Liste = request.data['Numbers']
        Message = request.data['Message']
        User = request.data['User']
        Date = request.data['Date']

        # Create a temporary file for the configuration
        message = {
            "type": "success",
            "message": "SMS envoye Par " + Users + " tous les numeros"
        }
        return JsonResponse(message)
# # Sending Sms To Directories with Gammu
# class Send_Directories_Sms(APIView):
#     def post(self, request):
#         Directory = request.data['Directory']
#         Message = request.data['Message']
#         User = request.data['User']
#         Date = request.data['Date']
#
#         # Create a temporary file for the configuration
#         temp_config_file = tempfile.NamedTemporaryFile(delete=False)
#         temp_config_file.write(CONFIG_CONTENT_2.encode())
#         temp_config_file.close()
#
#         # Create object for talking with phone
#         state_machine = gammu.StateMachine()
#         # Read the configuration from the given file
#         state_machine.ReadConfig(Filename=temp_config_file.name)
#         # Connect to the phone
#         state_machine.Init()
#
#         # Get all number liste from directory
#         directory = Directory.objects.filter(deleted_by__isnull=True).get(Directory_Id=Directory)
#         relation_numbers = Relation_Directory_Number.objects.filter(deleted_by__isnull=True, Directory=directory)
#         serialized_numbers = []
#         for number in relation_numbers:
#             serialized_numbers.append(serializers.RelationDirectoryNumberSerializer(number).data["Number"])
#         numbers_list = [number["Number"] for number in serialized_numbers]
#         if not Date:
#             success_count = 0
#             total_count = len(numbers_list)
#             for number in numbers_list:
#                 # Send a normal message if the message length is less than or equal to 160 characters
#                 if len(Message) <= 160:
#                     message = {
#                         "Text": Message,
#                         "SMSC": {"Location": 1},
#                         "Number": number,
#                     }
#                     # Actually send the message
#                     result = state_machine.SendSMS(message)
#                     if result:
#                         success_count += 1
#                 else:
#                     # Create SMS info structure
#                     smsinfo = {
#                         "Class": -1,
#                         "Unicode": False,
#                         "Entries": [
#                             {
#                                 "ID": "ConcatenatedTextLong",
#                                 "Buffer": Message
#                             }
#                         ],
#                     }
#                     # Encode messages
#                     encoded = gammu.EncodeSMS(smsinfo)
#                     # Send messages
#                     for message in encoded:
#                         # Fill in numbers
#                         message["SMSC"] = {"Location": 1}
#                         message["Number"] = number
#                         # Actually send the message
#                         result = state_machine.SendSMS(message)
#                         if result:
#                             success_count += 1
#             if success_count == total_count:
#                 message = {
#                     "message": "SMS envoye a tous les numeros"
#                 }
#             else:
#                 message = {
#                     "message": "Echec de l'envoi de certains SMS"
#                 }
#             state_machine.Terminate()
#             # Delete the temporary configuration file
#             os.remove(temp_config_file.name)
#             return JsonResponse(message)
#         else:
#             # Code to send message at the defined date
#             message = {
#                 "type": "success",
#                 "message": "Sms Programmé"
#             }
#             return JsonResponse(message)
# class Send_Mailing_List_Sms(APIView):
#     def post(self, request):
#
#         Mailing_List = request.data['Mailing_List']
#         Message = request.data['Message']
#         User = request.data['User']
#         Date = request.data['Date']
#
#         # Create a temporary file for the configuration
#         temp_config_file = tempfile.NamedTemporaryFile(delete=False)
#         temp_config_file.write(CONFIG_CONTENT_2.encode())
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
#         mailing_list = Mailing_List.objects.filter(deleted_by__isnull=True).get(Mailing_List_Id=Mailing_List)
#         # Access the path of the mailing list file
#         mailing_list_path = mailing_list.Mailing_List_Url.name
#         mailing_list_data = []
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
#                     if not Date:
#                         success_count = 0
#                         total_count = len(Numbers)
#                         for number in Numbers:
#                             # Send a normal message if the message length is less than or equal to 160 characters
#                             if len(Message) <= 160:
#                                 message = {
#                                     "Text": Message,
#                                     "SMSC": {"Location": 1},
#                                     "Number": number,
#                                 }
#                                 # Actually send the message
#                                 result = state_machine.SendSMS(message)
#                                 if result:
#                                     success_count += 1
#                             else:
#                                 # Create SMS info structure
#                                 smsinfo = {
#                                     "Class": -1,
#                                     "Unicode": False,
#                                     "Entries": [
#                                         {
#                                             "ID": "ConcatenatedTextLong",
#                                             "Buffer": Message
#                                         }
#                                     ],
#                                 }
#                                 # Encode messages
#                                 encoded = gammu.EncodeSMS(smsinfo)
#                                 # Send messages
#                                 for message in encoded:
#                                     # Fill in numbers
#                                     message["SMSC"] = {"Location": 1}
#                                     message["Number"] = number
#                                     # Actually send the message
#                                     result = state_machine.SendSMS(message)
#                                     if result:
#                                         success_count += 1
#                         if success_count == total_count:
#                             message = {
#                                 "message": "SMS envoye a tous les numeros"
#                             }
#                         else:
#                             message = {
#                                 "message": "Echec de l'envoi de certains SMS"
#                             }
#                         state_machine.Terminate()
#                         # Delete the temporary configuration file
#                         os.remove(temp_config_file.name)
#                         return JsonResponse(message)
#
#                     else:
#                         # Code to send message at the defined date
#                         message = {
#                             "type": "success",
#                             "message": "Sms Programmé"
#                         }
#                         return JsonResponse(message)
#                 elif len(first_row) == 2 and not Message:
#                     for row in csv_reader:
#                         phone_number = row[0].strip('""')
#                         message = row[1].strip('""')
#                         mailing_list_data.append({'Phone_Number': phone_number, 'Message': message})
#
#                     file_data = mailing_list_data
#                     if not Date:
#                         success_count = 0
#                         total_count = len(file_data)
#                         for item in file_data:
#                             phone_number = item['Phone_Number']
#                             message_l = item['Message']
#                             if len(message_l) <= 160:
#                                 message_data = {
#                                     "Text": message_l,
#                                     "SMSC": {"Location": 1},
#                                     "Number": phone_number,
#                                 }
#                                 # Actually send the message
#                                 result = state_machine.SendSMS(message_data)
#                                 if result:
#                                     success_count += 1
#                             else:
#                                 # Create SMS info structure
#                                 smsinfo = {
#                                     "Class": -1,
#                                     "Unicode": False,
#                                     "Entries": [
#                                         {
#                                             "ID": "ConcatenatedTextLong",
#                                             "Buffer": message_l
#                                         }
#                                     ],
#                                 }
#                                 # Encode messages
#                                 encoded = gammu.EncodeSMS(smsinfo)
#                                 # Send messages
#                                 for message in encoded:
#                                     # Fill in numbers
#                                     message["SMSC"] = {"Location": 1}
#                                     message["Number"] = phone_number
#                                     # Actually send the message
#                                     result = state_machine.SendSMS(message)
#                                     if result:
#                                         success_count += 1
#                         if success_count == total_count:
#                             message = {
#                                 "message": "SMS envoye a tous les numeros"
#                             }
#                         else:
#                             message = {
#                                 "message": "Echec de l'envoi de certains SMS"
#                             }
#                         state_machine.Terminate()
#                         # Delete the temporary configuration file
#                         os.remove(temp_config_file.name)
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
# # Get Modem  (Phone Info)
# def status(request):
#     # Execute the SQL query
#     with connection.cursor() as cursor:
#         query = """ SELECT * FROM smsdb.phones """
#         cursor.execute(query)
#         phone_info = cursor.fetchall()
#
#     # Format the result as a list of dictionaries
#     columns = [col[0] for col in cursor.description]
#     phone_info = [dict(zip(columns, row)) for row in phone_info]
#
#     # Return the phone information as JSON
#     return JsonResponse(phone_info, safe=False)
