from django.shortcuts import render
from django.contrib import messages

from MyApp.models import Entities


# Create your views here.
def index(request):
    return render(request, "layouts/index.html");


def entities(request):
    return render(request, "Entities/index.html");


def add_entity(request):
    if request.method == "POST":
        name_entities = request.POST['name_entities']
        description_entities = request.POST['description_entities']

        entities = Entities(Entity_Name=name_entities, Entity_Description=description_entities)

        entities.save()
        messages.success(request, "Entities Successefelly Added")
        return render(request, "layouts/index.html", {'entities': entities})

    return render(request, "Entities/index.html")
