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