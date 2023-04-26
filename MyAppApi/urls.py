from django.conf.urls.static import static
from django.urls import path, include
from . import views
from Project_SMS import settings


urlpatterns = [
    path('', views.index, name='index'),
    path('entities/', views.EntitiesDetail.as_view(), name='entity_list'),
    path('entities/<int:id>/', views.EntitiesInfo.as_view(), name='delete_entity'),
]
