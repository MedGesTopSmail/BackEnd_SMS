import os
import sys
# import gammu
import random
from django.utils import timezone
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from .models import Entities, Groups, Users, Number_List, Directory, Predefined_Message, Mailing_List, \
    Relation_Directory_Number
from . import serializers
from rest_framework import status
from django.http import JsonResponse
from .serializers import Mailing_ListSerializer


def index(request):
    return render(request, 'Layouts/index.html')

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
            obj = Groups.objects.get(Group_Id=id)
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
            obj = Groups.objects.get(Group_Id=id)
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
            obj = Groups.objects.get(Group_Id=id)
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
            relation_numbers = Relation_Directory_Number.objects.filter(deleted_by__isnull=True, Directory=directory).values_list('Number', flat=True)

            data = {
                "directory": serializers.DirectorySerializer(directory).data,
                "list_numbers": list(relation_numbers)
            }
            return JsonResponse(data)
        except Directory.DoesNotExist:
            message = {"message": "Directory non trouvé"}
            return JsonResponse(message, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id):
        try:
            obj = Directory.objects.filter(deleted_by__isnull=True).get(Directory_Id=id)
            serializer = serializers.DirectorySerializer(obj, data=request.data)
            if serializer.is_valid():
                directory_name = serializer.validated_data['Directory_Name']
                if Directory.objects.filter(Directory_Name=directory_name).filter(deleted_by__isnull=True).exists():
                    message = {
                        "type": "error",
                        "message": "Répertoire " + directory_name + " existe déjà",
                    }
                    return JsonResponse(message)
                serializer.save()
                data = serializer.data
                message = {
                    "type": "success",
                    "message": "Répertoire " + data.get("Directory_Name") + " modifié avec succes",
                    "id": data.get("Directory_Id")
                }
                return JsonResponse(message)
        except Directory.DoesNotExist:
            message = {"message": "Directory non trouver"}
            return JsonResponse(message, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, id):
        try:
            obj = Directory.objects.get(Directory_Id=id)
            serializer = serializers.DirectorySerializer(obj, data=request.data, partial=True)
            if serializer.is_valid():
                directory_name = serializer.validated_data['Directory_Name']
                if Directory.objects.filter(Directory_Name=directory_name).filter(deleted_by__isnull=True).exists():
                    message = {
                        "type": "error",
                        "message": "Répertoire " + directory_name + " existe déjà",
                    }
                    return JsonResponse(message)
                serializer.save()
                data = serializer.data
                message = {
                    "type": "success",
                    "message": "Répertoire " + data.get("Directory_Name") + " modifié avec succes",
                    "id": data.get("Directory_Id")
                }
                return JsonResponse(message)
        except Directory.DoesNotExist:
            message = {"message": "Directory not found"}
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

# Send Message with Gammu
def MessageSend(request):
    return render(request, 'Send_Message/index.html')


# class SendSMS(APIView):
#     def post(self, request):
#         # Get the recipient number and message from the POST data
#         recipient_number = request.POST.get('recipient_number')
#         recipient_text = request.POST.get('recipient_text')
#
#         # Create object for talking with phone
#         state_machine = gammu.StateMachine()
#
#         # Optionally load config file as defined by first parameter
#         if len(sys.argv) > 2:
#             # Read the configuration from given file
#             state_machine.ReadConfig(Filename='/etc/gammu-smsdrc-1' + sys.argv[1])
#             # Remove file name from args list
#             del sys.argv[1]
#         else:
#             # Read the configuration (~/.gammurc)
#             state_machine.ReadConfig()
#
#         # Check parameters
#         if not recipient_number:
#             return JsonResponse("Please provide a recipient number.")
#
#         # Connect to the phone
#         state_machine.Init()
#
#         # Prepare message data
#         # We tell that we want to use first SMSC number stored in phone
#         message = {
#             "Text": recipient_text,
#             "SMSC": {"Location": 1},
#             "Number": recipient_number,
#         }
#
#         # Actually send the message
#         state_machine.SendSMS(message)
#
#         return JsonResponse("SMS sent to {}".format(recipient_number))

# class SendSMS(APIView):
#     def post(self, request):
#         # Get the recipient number and message from the POST data
#         recipient_number = request.POST.get('recipient_number')
#         recipient_text = request.POST.get('recipient_text')
#
#         # Create object for talking with phone
#         state_machine = gammu.StateMachine()
#
#         # Optionally load config file as defined by first parameter
#         if len(sys.argv) > 2:
#             # Read the configuration from given file
#             state_machine.ReadConfig(Filename='/etc/gammu-smsdrc-1' + sys.argv[1])
#             # Remove file name from args list
#             del sys.argv[1]
#         else:
#             # Read the configuration (~/.gammurc)
#             state_machine.ReadConfig()
#
#         # Check parameters
#         if not recipient_number:
#             return JsonResponse("Please provide a recipient number.")
#
#         # Connect to the phone
#         state_machine.Init()
#
#         # Prepare message data
#         if len(recipient_text) <= 160:
#             # Send a normal message if the message length is less than or equal to 160 characters
#             message = {
#                 "Text": recipient_text,
#                 "SMSC": {"Location": 1},
#                 "Number": recipient_number,
#             }
#             # Actually send the message
#             state_machine.SendSMS(message)
#         else:
#             # Split the message into parts of 153 characters (GSM 7-bit encoding) or 134 characters (UCS2 encoding)
#             parts = gammu.EncodeSMS(recipient_text, 1)
#
#             # Calculate the number of messages
#             num_parts = len(parts)
#
#             # Initialize the current modem index to 0
#             current_modem_index = 0
#
#             # Loop over the message parts and send them using the available modems
#             for i, part in enumerate(parts):
#                 # Prepare message data
#                 message = {
#                     "UDH": part[0],
#                     "Text": part[1],
#                     "SMSC": {"Location": 1},
#                     "Number": recipient_number,
#                 }
#
#                 # Get the list of available modems
#                 modems = state_machine.GetConnectedGSMPhones()
#
#                 # Get the current modem
#                 current_modem = modems[current_modem_index]
#
#                 # Actually send the message using the current modem
#                 state_machine.SendSMS(message, current_modem)
#
#                 # Increment the current modem index and reset it to 0 if it exceeds the number of available modems
#                 current_modem_index = (current_modem_index + 1) % len(modems)
#
#         return JsonResponse("SMS sent to {}".format(recipient_number))


# def modem_status(request):
#     sm = gammu.StateMachine()
#     sm.ReadConfig()  # read the configuration file for Gammu
#     sm.Init()  # initialize the state machine
#
#     state = sm.GetSMSStatus()  # get the SMS status of the phone
#
#     return JsonResponse(state)


# def log_message(request):
#     sm = gammu.StateMachine()
#     sm.ReadConfig()  # read the configuration file for Gammu
#     sm.Init()  # initialize the state machine
#
#     sent_items = sm.GetSMS(sentfolder=1, folder=0)  # get the sent items from the phone
#
#     items_data = []
#     for item in sent_items:
#         items_data.append(item)
#
#     return JsonResponse({'sent_items': items_data})



# Mailing list View


class UploadMailingLists(APIView):
     def post(self, request):
         serializer = Mailing_ListSerializer(data=request.data)
         if serializer.is_valid():
             mailing_list = serializer.save()
             mailing_list.Mailing_List_File = request.FILES['Mailing_List_Url'].name
             mailing_list.save()

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

# class Authenticate(auth):
#     def login(self, request, username=None, password=None, **kwargs):
#         Users = get_user_model()
#         try:
#             user = Users.objects.get(User_Email=username)
#         except Users.DoesNotExist:
#             return None
#         else:
#             if user.check_password(password):
#                 return user
#         return None
#
#     def logout(self, request):
#         logout(request)
