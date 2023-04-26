from django.db import connection
from django.shortcuts import render, redirect
from django.contrib import messages
import random
import json
from .models import Entities

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .serializers import EntitiesSerializer


def index(request):
    return render(request, 'Layouts/index.html')


class EntitiesDetail(APIView):
    def get(self,request):
        obj = Entities.objects.all()
        serializer = EntitiesSerializer(obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self,request):
        serializer = EntitiesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)



class EntitiesInfo(APIView):
    def get(self, request, id):
        try:
            obj = Entities.objects.get(Entity_Id=id)
        except Entities.DoesNotExist:
            message = {"message":"not found"}
            return Response(message, status=status.HTTP_404_NOT_FOUND)
        serializer = EntitiesSerializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
        # return render(request, "Entities/index.html", {'entities': serializer.data})

    def put(self,request,id):
        try:
            obj = Entities.objects.get(Entity_Id=id)
        except Entities.DoesNotExist:
            message = {"message": "not found error"}
            return Response(message, status=status.HTTP_404_NOT_FOUND)

        serializer = EntitiesSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


    def patch(self,request, id):
        try:
            obj = Entities.objects.get(Entity_Id=id)
        except Entities.DoesNotExist:
            message = {"message": "not found error"}
            return Response(message, status=status.HTTP_404_NOT_FOUND)

        serializer = EntitiesSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request, id):
        try:
            obj = Entities.objects.get(Entity_Id=id)
        except Entities.DoesNotExist:
            message = {"message": "not found error"}
            return Response(message, status=status.HTTP_404_NOT_FOUND)
        obj.delete()
        return Response({"message":"Entity Deleted"}, status=status.HTTP_204_NO_CONTENT)

