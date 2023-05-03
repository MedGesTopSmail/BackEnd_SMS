from django.db import connection
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
import random
import json
# import gammu
from .models import Entities, Groups, Users, Number_List, Directory, Message
from . import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status



def index(request):
    return render(request, 'Layouts/index.html')


class EntitiesDetail(APIView):
    def get(self, request):
        obj = Entities.objects.all()
        serializer = serializers.EntitiesSerializer(obj, many=True)
        data = serializer.data
        return JsonResponse(data, safe=False)
    def post(self, request):
        serializer = serializers.EntitiesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            return JsonResponse(data, status=status.HTTP_201_CREATED)
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
            return JsonResponse(data, status=status.HTTP_200_OK)
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
            return JsonResponse(data, status=status.HTTP_200_OK)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            obj = Entities.objects.get(Entity_Id=id)
        except Entities.DoesNotExist:
            message = {"message": "Entity not found"}
            return JsonResponse(message, status=status.HTTP_404_NOT_FOUND)
        obj.delete()
        return JsonResponse({"message": "Entity Deleted"}, status=status.HTTP_204_NO_CONTENT)


class GroupsDetail(APIView):
    def get(self, request):
        obj = Groups.objects.all()
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
        obj = Users.objects.all()
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
        obj = Number_List.objects.all()
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
        obj = Directory.objects.all()
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
        obj = Message.objects.all()
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

# class SMSAPIView(APIView):
#     def post(self, request):
#         recipient = request.data.get('recipient')
#         message = request.data.get('message')
#
#         # Configuration de gammu
#         sm = gammu.StateMachine()
#         sm.ReadConfig()
#         sm.Init()
#
#         # Envoi du SMS
#         message = {
#             'Text': message,
#             'SMSC': {'Location': 1},
#             'Number': recipient,
#         }
#         sm.SendSMS(message)
#
#         # Enregistrement dans la base de données
#         sms = SMS.objects.create(
#             recipient=recipient,
#             message=message,
#         )
#
#         return Response(status=status.HTTP_201_CREATED)