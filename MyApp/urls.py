from django.conf.urls.static import static
from django.urls import path, include
from Project_SMS import settings
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('entities', views.entities, name="entities.index"),
    path('add_entity', views.add_entity, name="add_entity"),
]
