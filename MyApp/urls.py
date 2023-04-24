from django.conf.urls.static import static
from django.urls import path, include
from Project_SMS import settings
from .views import EntitiesDetail

urlpatterns = [
    path('entities/', EntitiesDetail.as_view(), name="entities"),

]
