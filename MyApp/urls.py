from django.conf.urls.static import static
from django.urls import path, include
from Project_SMS import settings
from . import views

urlpatterns = [
    path('', views.index, name="index"),
]
