from django.conf.urls.static import static
from django.urls import path, include
from . import views
from Project_SMS import settings


urlpatterns = [
    path('', views.index, name='index'),

    # CRUD Entities
    path('entities/', views.EntitiesDetail.as_view(), name='Entities_Detail'),
    path('entities/<int:id>/', views.EntitiesInfo.as_view(), name='Entities_Info'),

    # CRUD Groups
    path('groups/', views.GroupsDetail.as_view(), name='Groups_Detail'),
    path('groups/<int:id>/', views.GroupsInfo.as_view(), name='Groups_Info'),

    # CRUD Users
    path('users/', views.UsersDetail.as_view(), name='Users_Detail'),
    path('users/<int:id>/', views.UsersInfo.as_view(), name='Users_Info'),

    # CRUD NumberList
    path('number_list/', views.NumberListDetail.as_view(), name='Number_Detail'),
    path('number_list/<int:id>/', views.NumberListInfo.as_view(), name='Number_Info'),

    # CRUD Directory
    path('directory/', views.DirectoryDetail.as_view(), name='Directory_Detail'),
    path('directory/<int:id>/', views.DirectoryInfo.as_view(), name='Directory_Info'),

    # CRUD Message
    path('message/', views.MessageDetail.as_view(), name='Message_Detail'),
    path('message/<int:id>/', views.MessageInfo.as_view(), name='Message_Info'),

    # Upload Mailing List
    path('upload-mailing/', views.UploadMailingLists.as_view(), name='Upload-MailingList'),

    # Send Message Gammu
    path('send_message/', views.MessageSend, name='Send_Message'),

    # Generate Number For Row Table
    path('entity_generate/', views.entity_generate, name='EntityNumber_Generate'),
    path('group_generate/', views.group_generate, name='GroupNumber_Generate'),
    path('user_generate/', views.user_generate, name='UserNumber_Generate'),
]
