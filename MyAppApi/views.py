import os
import sys
import random

from django.utils import timezone

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView

# import gammu
from .models import Entities, Groups, Users, Number_List, Directory, Message, Mailing_List
from . import serializers
from rest_framework import status
from django.http import JsonResponse
from .forms import MailingListForm


def index(request):
    return render(request, 'Layouts/index.html')


def entity_generate(self):
    Entity_Number = f'ENT{random.randint(0, 9999):04}'
    while Entities.objects.filter(Entity_Number=Entity_Number).exists():
        Entity_Number = f'ENT{random.randint(0, 9999):04}'
    data = {
        "Entity_Number": Entity_Number,
    }
    return JsonResponse(data)


def group_generate(self):
    Group_Number = f'GR{random.randint(0, 9999):04}'
    while Groups.objects.filter(Group_Number=Group_Number).exists():
        Group_Number = f'GR{random.randint(0, 9999):04}'
    data = {
        "Group_Number": Group_Number,
    }
    return JsonResponse(data)


def user_generate(self):
    User_Number = f'USR{random.randint(0, 9999):04}'
    while Users.objects.filter(User_Number=User_Number).exists():
        User_Number = f'USR{random.randint(0, 9999):04}'
    data = {
        "User_Number": User_Number,
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
            serializer.save()
            data = serializer.data
            message = {
                "type": "success",
                "message": "Entite " + data.get("Entity_Name") + " ajouter avec succes",
            }
            return JsonResponse(message)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EntitiesInfo(APIView):
    def get(self, request, id):
        try:
            obj = Entities.objects.get(Entity_Id=id)
        except Entities.DoesNotExist:
            message = {"message": "Entity not found"}
            return JsonResponse(message, status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.EntitiesSerializer(obj)
        data = serializer.data
        return JsonResponse(data, safe=False)

    def put(self, request, id):
        try:
            obj = Entities.objects.get(Entity_Id=id)
        except Entities.DoesNotExist:
            message = {"message": "Entity not found"}
            return JsonResponse(message, status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.EntitiesSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            message = {
                "type": "success",
                "message": "Entite " + data.get("Entity_Name") + " modifier avec succes",
            }
            return JsonResponse(message)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id):
        try:
            obj = Entities.objects.get(Entity_Id=id)
        except Entities.DoesNotExist:
            message = {"message": "Entity not found"}
            return JsonResponse(message, status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.EntitiesSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            message = {
                "type": "success",
                "message": "Entite " + data.get("Entity_Name") + " modifier avec succes",
            }
            return JsonResponse(message)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @csrf_exempt
    def delete(self, request, id):
        try:
            obj = Entities.objects.get(Entity_Id=id)
        except Entities.DoesNotExist:
            message = {"message": "Entity not found"}
            return JsonResponse(message, status=status.HTTP_404_NOT_FOUND)
        obj.deleted_at = timezone.now()
        obj.deleted_by = 1
        obj.save()
        message = {
            "type": "success",
            "message": "Entite Supprimer avec succes",
        }
        return JsonResponse(message, status=status.HTTP_204_NO_CONTENT)


class GroupsDetail(APIView):
    def get(self, request):
        obj = Groups.objects.filter(deleted_by__isnull=True)
        serializer = serializers.GroupsSerializer(obj, many=True)
        data = serializer.data
        return JsonResponse(data, safe=False)

    def post(self, request):
        serializer = serializers.GroupsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            return JsonResponse(data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GroupsInfo(APIView):
    def get(self, request, id):
        try:
            obj = Groups.objects.get(Group_Id=id)
        except Groups.DoesNotExist:
            message = {"message": "Group not found"}
            return JsonResponse(message, status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.GroupsSerializer(obj)
        data = serializer.data
        return JsonResponse(data, safe=False)

    def put(self, request, id):
        try:
            obj = Groups.objects.get(Group_Id=id)
        except Groups.DoesNotExist:
            message = {"message": "Group not found"}
            return JsonResponse(message, status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.GroupsSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            return JsonResponse(data, status=status.HTTP_200_OK)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id):
        try:
            obj = Groups.objects.get(Group_Id=id)
        except Groups.DoesNotExist:
            message = {"message": "Group not found"}
            return JsonResponse(message, status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.GroupsSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            return JsonResponse(data, status=status.HTTP_200_OK)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            obj = Groups.objects.get(Group_Id=id)
        except Groups.DoesNotExist:
            message = {"message": "Group not found"}
            return JsonResponse(message, status=status.HTTP_404_NOT_FOUND)
        obj.delete()
        return JsonResponse({"message": "Group Deleted"}, status=status.HTTP_204_NO_CONTENT)


class UsersDetail(APIView):
    def get(self, request):
        obj = Users.objects.filter(deleted_by__isnull=True)
        serializer = serializers.UsersSerializer(obj, many=True)
        data = serializer.data
        return JsonResponse(data, safe=False)

    def post(self, request):
        serializer = serializers.UsersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            return JsonResponse(data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsersInfo(APIView):
    def get(self, request, id):
        try:
            obj = Users.objects.get(User_Id=id)
        except Users.DoesNotExist:
            message = {"message": "User not found"}
            return JsonResponse(message, status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.UsersSerializer(obj)
        data = serializer.data
        return JsonResponse(data, safe=False)
        # return render(request, "Entities/index.html", {'entities': serializer.data})

    def put(self, request, id):
        try:
            obj = Users.objects.get(User_Id=id)
        except Users.DoesNotExist:
            message = {"message": "User not found"}
            return JsonResponse(message, status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.UsersSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            return JsonResponse(data, status=status.HTTP_200_OK)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id):
        try:
            obj = Users.objects.get(User_Id=id)
        except Users.DoesNotExist:
            message = {"message": "User not found"}
            return JsonResponse(message, status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.UsersSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            return JsonResponse(data, status=status.HTTP_200_OK)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            obj = Users.objects.get(User_Id=id)
        except Users.DoesNotExist:
            message = {"message": "not found error"}
            return JsonResponse(message, status=status.HTTP_404_NOT_FOUND)
        obj.delete()
        return JsonResponse({"message": "User Deleted"}, status=status.HTTP_204_NO_CONTENT)


class NumberListDetail(APIView):
    def get(self, request):
        obj = Number_List.objects.filter(deleted_by__isnull=True)
        serializer = serializers.NumberListSerializer(obj, many=True)
        data = serializer.data
        return JsonResponse(data, safe=False)

    def post(self, request):
        serializer = serializers.NumberListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            return JsonResponse(data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NumberListInfo(APIView):
    def get(self, request, id):
        try:
            obj = Number_List.objects.get(Number_Id=id)
        except Number_List.DoesNotExist:
            message = {"message": "Number not found"}
            return JsonResponse(message, status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.NumberListSerializer(obj)
        data = serializer.data
        return JsonResponse(data, safe=False)
        # return render(request, "Entities/index.html", {'entities': serializer.data})

    def put(self, request, id):
        try:
            obj = Number_List.objects.get(Number_Id=id)
        except Number_List.DoesNotExist:
            message = {"message": "Number not found"}
            return JsonResponse(message, status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.NumberListSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            return JsonResponse(data, status=status.HTTP_200_OK)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id):
        try:
            obj = Number_List.objects.get(Number_Id=id)
        except Number_List.DoesNotExist:
            message = {"message": "Number not found"}
            return JsonResponse(message, status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.NumberListSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            return JsonResponse(data, status=status.HTTP_200_OK)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            obj = Number_List.objects.get(Number_Id=id)
        except Number_List.DoesNotExist:
            message = {"message": "Number not found"}
            return JsonResponse(message, status=status.HTTP_404_NOT_FOUND)
        obj.delete()
        return JsonResponse({"message": "Number Deleted"}, status=status.HTTP_204_NO_CONTENT)


class DirectoryDetail(APIView):
    def get(self, request):
        obj = Directory.objects.filter(deleted_by__isnull=True)
        serializer = serializers.DirectorySerializer(obj, many=True)
        data = serializer.data
        return JsonResponse(data, safe=False)

    def post(self, request):
        serializer = serializers.DirectorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            return JsonResponse(data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DirectoryInfo(APIView):
    def get(self, request, id):
        try:
            obj = Directory.objects.get(Directory_Id=id)
        except Directory.DoesNotExist:
            message = {"message": "Directory not found"}
            return JsonResponse(message, status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.DirectorySerializer(obj)
        data = serializer.data
        return JsonResponse(data, safe=False)
        # return render(request, "Entities/index.html", {'entities': serializer.data})

    def put(self, request, id):
        try:
            obj = Directory.objects.get(Directory_Id=id)
        except Directory.DoesNotExist:
            message = {"message": "Directory not found"}
            return JsonResponse(message, status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.DirectorySerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            return JsonResponse(data, status=status.HTTP_200_OK)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id):
        try:
            obj = Directory.objects.get(Directory_Id=id)
        except Directory.DoesNotExist:
            message = {"message": "Directory not found"}
            return JsonResponse(message, status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.DirectorySerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            return JsonResponse(data, status=status.HTTP_200_OK)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            obj = Directory.objects.get(Directory_Id=id)
        except Directory.DoesNotExist:
            message = {"message": "Directory not found"}
            return JsonResponse(message, status=status.HTTP_404_NOT_FOUND)
        obj.delete()
        return JsonResponse({"message": "Directory Deleted"}, status=status.HTTP_204_NO_CONTENT)


class MessageDetail(APIView):
    def get(self, request):
        obj = Message.objects.filter(deleted_by__isnull=True)
        serializer = serializers.MessageSerializer(obj, many=True)
        data = serializer.data
        return JsonResponse(data, safe=False)

    def post(self, request):
        serializer = serializers.MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            return JsonResponse(data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MessageInfo(APIView):
    def get(self, request, id):
        try:
            obj = Message.objects.get(Message_Id=id)
        except Message.DoesNotExist:
            message = {"message": "Message not found"}
            return JsonResponse(message, status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.MessageSerializer(obj)
        data = serializer.data
        return JsonResponse(data, safe=False)
        # return render(request, "Entities/index.html", {'entities': serializer.data})

    def put(self, request, id):
        try:
            obj = Message.objects.get(Message_Id=id)
        except Message.DoesNotExist:
            message = {"message": "Message not found"}
            return JsonResponse(message, status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.MessageSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            return JsonResponse(data, status=status.HTTP_200_OK)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id):
        try:
            obj = Message.objects.get(Message_Id=id)
        except Message.DoesNotExist:
            message = {"message": "Message not found"}
            return JsonResponse(message, status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.MessageSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            return JsonResponse(data, status=status.HTTP_200_OK)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            obj = Message.objects.get(Message_Id=id)
        except Message.DoesNotExist:
            message = {"message": "Message not found"}
            return JsonResponse(message, status=status.HTTP_404_NOT_FOUND)
        obj.delete()
        return JsonResponse({"message": "Message Deleted"}, status=status.HTTP_204_NO_CONTENT)


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

# class SendSMS_Multipart(APIView):
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

class UploadMailingLists(APIView):
    def post(self, request):
        form = MailingListForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the uploaded file
            my_file = form.save(commit=False)
            my_file.save()

            # Update the URL field with the file's URL
            my_file.Mailing_List_Name = request.POST['Mailing_List_Name']
            my_file.Mailing_List_File = request.FILES['Mailing_List_Url'].name
            my_file.save()

            # Return a JSON response with the file URL and a success message
            message = {
                'message': 'File Upload Successfully',
                'file_url': my_file.Mailing_List_Url.url
            }
            return JsonResponse(message, status=status.HTTP_201_CREATED)
        else:
            # Return a JSON response with an error message
            message = {
                'message': 'Upload Fail',
                'errors': form.errors.as_json()
            }
            return JsonResponse(message, status=status.HTTP_400_BAD_REQUEST)
