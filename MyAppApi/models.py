import base64

from django.db import models
import random
from django.contrib.auth.hashers import make_password


# Create your models here.

# Create Table Entities
class Entities(models.Model):
    Entity_Id = models.AutoField(primary_key=True)
    Entity_Number = models.CharField(max_length=500)
    Entity_Name = models.CharField(max_length=500)
    Entity_Description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_by = models.IntegerField(null=True, default=None)
    deleted_at = models.DateTimeField(null=True, default=None)

    class Meta:
        db_table = "entities"

    @classmethod
    def create_initial_entities(cls):
        admin_entity = cls.objects.create(
            Entity_Number="ENT0001",
            Entity_Name="Entite Administrateur",
            Entity_Description="Description Entite Administrateur",
        )
        return admin_entity


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
    @classmethod
    def create_initial_groups(cls):
        admin_groups = cls.objects.create(
            Group_Number="GR0001",
            Group_Name="Groupe Administrateur",
            Group_Description="Description Groupe Administrateur",
            Entity="1"
        )
        return admin_groups


class Users(models.Model):
    ROLE_CHOICES = (
        ('Member', 'Member'),
        ('Administrateur', 'Administrateur'),
        ('Super Administrateur', 'Super Administrateur')
    )
    User_Id = models.AutoField(primary_key=True)
    User_Number = models.CharField(max_length=500)
    User_First_Name = models.CharField(max_length=500)
    User_Last_Name = models.CharField(max_length=500)
    User_Role = models.CharField(max_length=500, choices=ROLE_CHOICES)
    User_Email = models.CharField(max_length=500)
    User_Password = models.CharField(max_length=500)
    User_Password_Crypt = models.CharField(max_length=500)
    Group = models.ForeignKey(Groups, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_by = models.IntegerField(null=True, default=None)
    deleted_at = models.DateTimeField(null=True, default=None)

    class Meta:
        db_table = "users"

    def save(self, *args, **kwargs):
        # Hash the password in make_password and save it to User_Password field
        self.User_Password = make_password(self.User_Password)
        # Encode the hashed password in base64 and save it to User_Password_Crypt field
        self.User_Password_Crypt = base64.b85encode(self.User_Password_Crypt.encode("utf-8"), pad=False)
        super(Users, self).save(*args, **kwargs)

    @classmethod
    def create_initial_users(cls):
        admin_users = cls.objects.create(
            User_Number="USR0001",
            User_First_Name="Mohammed",
            User_Last_Name="Ennouaim",
            User_Role="Super Administrateur",
            User_Email="ennouaim@gestop.ma",
            User_Password="pbkdf2_sha256$600000$SzGGIMXtZfNz1rcry4eUfA$ruHqOsBErvhSQwdImVXHix0L+fDKp0sv3uq09AQa4qk=",
            User_Password_Crypt="b'O=V<7Zf-z0IR'",
            Group="1"
        )
        return admin_users

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
    Directory_Number = models.CharField(max_length=500)
    Directory_Description = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_by = models.IntegerField(null=True, default=None)
    deleted_at = models.DateTimeField(null=True, default=None)

    class Meta:
        db_table = "directory"


class Relation_Directory_Number(models.Model):
    Relation_Id = models.AutoField(primary_key=True)
    Directory = models.ForeignKey(Directory, on_delete=models.CASCADE)
    Number = models.ForeignKey(Number_List, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_by = models.IntegerField(null=True, default=None)
    deleted_at = models.DateTimeField(null=True, default=None)

    class Meta:
        db_table = "relation_directory_number"


class Mailing_List(models.Model):
    Mailing_List_Id = models.AutoField(primary_key=True)
    Mailing_List_Name = models.CharField(max_length=500)
    Mailing_List_File = models.CharField(max_length=500)
    Mailing_List_Url = models.FileField(upload_to='media/mailing_list/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_by = models.IntegerField(null=True, default=None)
    deleted_at = models.DateTimeField(null=True, default=None)

    class Meta:
        db_table = "mailing_list"


class Predefined_Message(models.Model):
    Message_Id = models.AutoField(primary_key=True)
    Message_Name = models.CharField(max_length=500)
    Message_Text = models.CharField(max_length=500)
    Message_Language = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_by = models.IntegerField(null=True, default=None)
    deleted_at = models.DateTimeField(null=True, default=None)

    class Meta:
        db_table = "predefined_message"


class Log_Message(models.Model):
    Send_Back_CHOICES = (
        ('True', 'True'),
        ('False', 'False')
    )
    Id = models.AutoField(primary_key=True)
    Recipient = models.CharField(max_length=500)
    Modem = models.CharField(max_length=500)
    Type_Envoi = models.CharField(max_length=500)
    Status = models.CharField(max_length=500)
    Message = models.CharField(max_length=500)
    Send_Back = models.CharField(max_length=500, null=True, default=None, choices=Send_Back_CHOICES)
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


class Roles(models.Model):
    Id = models.AutoField(primary_key=True)
    Role_Name = models.CharField(max_length=500)
    Role_Description = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_by = models.IntegerField(null=True, default=None)
    deleted_at = models.DateTimeField(null=True, default=None)

    class Meta:
        db_table = "roles"
    @classmethod
    def create_initial_roles(cls):
        admin_role = cls.objects.create(
            Role_Name="Administrateur",
            Role_Description="Administrateur role"
        )
        super_admin_role = cls.objects.create(
            Role_Name="Super Admin",
            Role_Description="Super Administrateur role"
        )
        member_role = cls.objects.create(
            Role_Name="Member",
            Role_Description="Member role"
        )
        return admin_role, super_admin_role, member_role


class Role_User(models.Model):
    Id = models.AutoField(primary_key=True)
    Role = models.ForeignKey(Roles, on_delete=models.CASCADE)
    User = models.ForeignKey(Users, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "role_user"


class Permissions(models.Model):
    Id = models.AutoField(primary_key=True)
    Permission_Name = models.CharField(max_length=500)
    Permission_Description = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_by = models.IntegerField(null=True, default=None)
    deleted_at = models.DateTimeField(null=True, default=None)

    class Meta:
        db_table = "permissions"


class Permission_User(models.Model):
    Id = models.AutoField(primary_key=True)
    Permission = models.ForeignKey(Permissions, on_delete=models.CASCADE)
    User = models.ForeignKey(Users, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "permission_user"


class Email_To_Sms(models.Model):
    Id = models.AutoField(primary_key=True)
    Client = models.CharField(max_length=500)
    HostName = models.CharField(max_length=500)
    Email_Server = models.CharField(max_length=500)
    Password_Server = models.CharField(max_length=500)
    Port = models.CharField(max_length=500)
    Recipient = models.CharField(max_length=500)
    Email_User = models.CharField(max_length=500)
    Password_User = models.CharField(max_length=500)
    Reload_Time = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "email_to_sms"