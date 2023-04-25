from django.db import connection
from django.shortcuts import render, redirect
from django.contrib import messages
import random
from .models import Entities

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .serializers import EntitiesSerializer




# Create your views here.
def Index(request):
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
        return render(request, "Entities/index.html", {'entities': serializer.data})

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
        return Response({"message": "Entities Deleted"}, status=status.HTTP_204_NO_CONTENT)



# def entities(request):
#     all_entities = Entities.objects.all()
#     return render(request, "Entities/index.html", {'all_entities': all_entities})
#
#
# def add_entity(request):
#     return render(request, "Entities/add.html")
#
#
# def store_entity(request):
#     if request.method == "POST":
#         entity_name = request.POST['entity_name']
#         entity_description = request.POST['entity_description']
#
#         existing_tags = Entities.objects.values_list('entity_number', flat=True)
#         entity_number = f'ENT{random.randint(0, 9999999):04}'
#         while entity_number in existing_tags:
#             entity_number = f'ENT{random.randint(0, 9999999):04}'
#
#         entities = Entities(Entity_Name=entity_name, Entity_Nunber=entity_number, Entity_Description=entity_description)
#         entities.save()
#         messages.success(request, "Entities Successfully Added")
#         return render(request, "layouts/index.html", {'entities': entities})
#     else:
#         messages.error(request, "Something Wrong")
#         return render(request, "Entities/index.html")
#
# def edit_entity(request, id):
#     entity = Entities.objects.get(Entity_Id=id)
#     return render(request, "Entities/edit.html", {'entity': entity})
#
#
# def update_entity(request, id):
#     if request.method == "POST":
#         entity_name = request.POST['entity_name']
#         entity_description = request.POST['entity_description']
#
#         entity = Entities.objects.get(id=id)
#
#         if request.method == "POST":
#             entity.name = request.POST['name_entities']
#             entity.description = request.POST['description_entities']
#             entity.save()
#
#             messages.success(request, "Entity updated successfully.")
#             return redirect('entities', id=entity.id)
#
#         context = {'entity': entity}
#         return render(request, 'update_entity.html', context)
