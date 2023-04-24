from django.db import models


# Create your models here.

# Create Table Entities
class Entities(models.Model):
    Entity_Id = models.AutoField(primary_key=True)
    Entity_Number = models.CharField(max_length=500)
    Entity_Name = models.CharField(max_length=500)
    Entity_Description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "Entities"


# # Create Table Groups
# class Groups(models.Model):
#     Group_Id = models.AutoField(primary_key=True)
#     Group_Name = models.CharField(max_length=500)
#     Entity = models.ForeignKey(Entities, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     deleted_by = models.IntegerField(null=True, blank=True)
#     deleted_at = models.DateTimeField(null=True, blank=True)
#
#     class Meta:
#         db_table = "Groups"
#
#
# # Create Table Users
# class Users(models.Model):
#     User_Id = models.AutoField(primary_key=True)
#     First_Name = models.CharField(max_length=500)
#     Last_Name = models.CharField(max_length=500)
#     User_Number = models.CharField(max_length=500)
#     User_Group = models.ForeignKey(Groups, on_delete=models.CASCADE)
#     User_Role = models.CharField(max_length=500, default='NULL')
#     User_Email = models.CharField(max_length=500)
#     User_Password = models.CharField(max_length=500)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     deleted_by = models.IntegerField(null=True, blank=True)
#     deleted_at = models.DateTimeField(null=True, blank=True)
#
#     class Meta:
#         db_table = "Users"
#
#     def __str__(self):
#         return self.First_Name