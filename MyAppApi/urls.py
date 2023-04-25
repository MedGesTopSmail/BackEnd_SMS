from django.conf.urls.static import static
from django.urls import path, include
from Project_SMS import settings
from .views import EntitiesDetail, EntitiesInfo, Index

urlpatterns = [
    path('', Index, name=""),
    path('entities/', EntitiesDetail.as_view(), name="entities"),
    path('entities/<int:id>', EntitiesInfo.as_view(), name="entities"),
]
