from django.db import migrations

def insert_initial_data(apps, schema_editor):
    Entities = apps.get_model('MyAppApi', 'Entities')
    Groups = apps.get_model('MyAppApi', 'Groups')
    User = apps.get_model('MyAppApi', 'Users')
    Role = apps.get_model('MyAppApi', 'Roles')

    entity = Entities.objects.create(
        Entity_Number="ENT0001",
        Entity_Name="Entite Administrateur",
        Entity_Description="Description Entite Administrateur",
    )

    group = Groups.objects.create(
        Group_Number="GR0001",
        Group_Name="Groupe Administrateur",
        Group_Description="Description Groupe Administrateur",
        Entity=entity
    )

    User.objects.create(
        User_Number="USR0001",
        User_First_Name="Mohammed",
        User_Last_Name="Ennouaim",
        User_Role="Super Administrateur",
        User_Email="ennouaim@gestop.ma",
        User_Password="pbkdf2_sha256$600000$SzGGIMXtZfNz1rcry4eUfA$ruHqOsBErvhSQwdImVXHix0L+fDKp0sv3uq09AQa4qk=",
        User_Password_Crypt="b'O=V<7Zf-z0IR'",
        Group=group
    )

    Role.objects.create(
        Role_Name="Super Admin",
        Role_Description="Super Administrateur role"
    )
    Role.objects.create(
        Role_Name="Administrateur",
        Role_Description="Administrateur role"
    )
    Role.objects.create(
        Role_Name="Member",
        Role_Description="Member role"
    )

class Migration(migrations.Migration):

    dependencies = [
        ('MyAppApi', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(insert_initial_data),
    ]
