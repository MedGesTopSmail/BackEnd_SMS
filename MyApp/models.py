from django.db import models


# Create your models here.

# Create Table Entities
class Entities(models.Model):
    Entity_Id = models.AutoField(primary_key=True)
    Entity_Name = models.CharField(max_length=500)
    Entity_Description = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Entities"


# Create Table Groups
class Groups(models.Model):
    Group_Id = models.AutoField(primary_key=True)
    Group_Name = models.CharField(max_length=500)
    Entity = models.ForeignKey(Entities, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Groups"


# Create Table Users
class Users(models.Model):
    User_Id = models.AutoField(primary_key=True)
    First_Name = models.CharField(max_length=500)
    Last_Name = models.CharField(max_length=500)
    Group = models.ForeignKey(Groups, on_delete=models.CASCADE)
    Role = models.CharField(max_length=500)
    Date_Of_Joining = models.DateField()
    Email_User = models.CharField(max_length=500)
    Password_User = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Users"

    def __str__(self):
        return self.FirstName

    objects = models.Manager()
