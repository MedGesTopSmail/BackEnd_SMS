from django.conf.urls.static import static
from django.urls import path, include
from . import views
from django.views.decorators.csrf import csrf_exempt
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
    path('numbers/', views.NumberListDetail.as_view(), name='Number_Detail'),
    path('numbers/<int:id>/', views.NumberListInfo.as_view(), name='Number_Info'),

    # CRUD Directory
    path('directories/', views.DirectoryDetail.as_view(), name='Directory_Detail'),
    path('directories/<int:id>/', views.DirectoryInfo.as_view(), name='Directory_Info'),

    # CRUD Message
    path('predefined_message/', views.MessageDetail.as_view(), name='Message_Detail'),
    path('predefined_message/<int:id>/', views.MessageInfo.as_view(), name='Message_Info'),

    # CRUD Message
    path('mailing_list/', views.Mailing_ListDetail.as_view(), name='Mailing_ListDetail'),
    path('mailing_list/<int:id>/', views.Mailing_ListInfo.as_view(), name='Mailing_ListInfo'),

    # CRUD Traceability Message
    path('log_message/', views.LogMessage.as_view(), name='Log_Message'),

    # Generate Number For Row Table
    path('generate/<str:tag>', views.generate, name='Generate'),

    # Authentication
    path('login/', views.login.as_view(), name='login'),
    path('logout', views.logout, name='logout'),

    # Send Sms With Gammu
    # path('send_normal_sms/', views.Send_Normal_Sms.as_view(), name='Send_Sms_Normal'),
    # path('send_directories_sms/', views.Send_Directories_Sms.as_view(), name='Send_Sms_Directories'),
    # path('send_mailing_list_sms/', views.Send_Mailing_List_Sms.as_view(), name='Send_Sms_Mailing_List'),
    # path('send_link_sms/<str:email>/<str:password>/<str:number>/<str:message>/', csrf_exempt(views.Send_Link_Sms), name='Send_Link_Sms'),


    # Info Modem Gammu
    # path('status/', views.status, name='modem_status'),



]
