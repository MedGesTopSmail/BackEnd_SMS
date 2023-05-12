from django.db import models
import random


# Create your models here.

# Create Table Entities
class Entities(models.Model):
    Entity_Id = models.AutoField(primary_key=True)
    Entity_Number = models.CharField(max_length=8)
    Entity_Name = models.CharField(max_length=500)
    Entity_Description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_by = models.IntegerField(null=True, default=None)
    deleted_at = models.DateTimeField(null=True, default=None)

    class Meta:
        db_table = "entities"


class Groups(models.Model):
    Group_Id = models.AutoField(primary_key=True)
    Group_Number = models.CharField(max_length=500)
    Group_Name = models.CharField(max_length=500)
    Group_Description = models.TextField(blank=True)
    Entity = models.ForeignKey(Entities, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_by = models.IntegerField(null=True, default=None)
    deleted_at = models.DateTimeField(null=True, default=None)

    class Meta:
        db_table = "groups"


class Users(models.Model):
    ROLE_CHOICES = (
        ('Member', 'Member'),
        ('Administrateur', 'Administrateur')
        # ('Super Administrateur', 'Super Administrateur')
    )
    # PERMISSION_CHOICES = (
    #     ('Add', 'Add'),
    #     ('View', 'View'),
    #     ('Edit', 'Edit'),
    #     ('Delete', 'Delete')
    # )
    User_Id = models.AutoField(primary_key=True)
    User_Number = models.CharField(max_length=500)
    User_First_Name = models.CharField(max_length=500)
    User_Last_Name = models.CharField(max_length=500)
    User_Role = models.CharField(max_length=500, choices=ROLE_CHOICES)
    # User_Permissions = models.CharField(max_length=500, choices=PERMISSION_CHOICES)
    User_Email = models.CharField(max_length=500)
    User_Password = models.CharField(max_length=500)
    Group = models.ForeignKey(Groups, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_by = models.IntegerField(null=True, default=None)
    deleted_at = models.DateTimeField(null=True, default=None)

    class Meta:
        db_table = "users"


class Number_List(models.Model):
    Number_Id = models.AutoField(primary_key=True)
    Number_Name = models.CharField(max_length=500)
    Number = models.CharField(max_length=500)
    Number_Email = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_by = models.IntegerField(null=True, default=None)
    deleted_at = models.DateTimeField(null=True, default=None)

    class Meta:
        db_table = "number_list"


class Directory(models.Model):
    Directory_Id = models.AutoField(primary_key=True)
    Directory_Name = models.CharField(max_length=500)
    Directory_Description = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_by = models.IntegerField(null=True, default=None)
    deleted_at = models.DateTimeField(null=True, default=None)

    class Meta:
        db_table = "directory"


class Directory_Number(models.Model):
    Directory = models.ForeignKey(Directory, on_delete=models.CASCADE)
    Number = models.ForeignKey(Number_List, on_delete=models.CASCADE)

    class Meta:
        db_table = "directory_number"
        unique_together = ('Directory', 'Number',)


class Mailing_List(models.Model):
    Mailing_List_Id = models.AutoField(primary_key=True)
    Mailing_List_Name = models.CharField(max_length=500)
    Mailing_List_File = models.CharField(max_length=500)
    Mailing_List_Url = models.FileField(upload_to='MyAppApi/Static/Media/Files/Mailing_List/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_by = models.IntegerField(null=True, default=None)
    deleted_at = models.DateTimeField(null=True, default=None)

    class Meta:
        db_table = "mailing_list"


class Message(models.Model):
    Message_Id = models.AutoField(primary_key=True)
    Message_Name = models.CharField(max_length=500)
    Message_Text = models.CharField(max_length=500)
    Message_Language = models.CharField(max_length=500)
    User = models.ForeignKey(Users, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_by = models.IntegerField(null=True, default=None)
    deleted_at = models.DateTimeField(null=True, default=None)

    class Meta:
        db_table = "message"


class Log_Message(models.Model):
    Id = models.AutoField(primary_key=True)
    Recipient = models.CharField(max_length=500)
    Modem = models.CharField(max_length=500)
    Message = models.CharField(max_length=500)
    User = models.ForeignKey(Users, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_by = models.IntegerField(null=True, default=None)
    deleted_at = models.DateTimeField(null=True, default=None)

    class Meta:
        db_table = "log_message"


class Log_App(models.Model):
    Id = models.AutoField(primary_key=True)
    Operation = models.CharField(max_length=500)
    Table = models.CharField(max_length=500)
    Object = models.CharField(max_length=500)
    User = models.ForeignKey(Users, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_by = models.IntegerField(null=True, default=None)
    deleted_at = models.DateTimeField(null=True, default=None)

    class Meta:
        db_table = "log_app"
