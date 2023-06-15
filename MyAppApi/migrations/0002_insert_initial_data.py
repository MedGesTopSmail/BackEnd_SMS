from django.db import migrations


def insert_initial_data(apps, schema_editor):
    Entities = apps.get_model('MyAppApi', 'Entities')
    Groups = apps.get_model('MyAppApi', 'Groups')
    User = apps.get_model('MyAppApi', 'Users')
    Role = apps.get_model('MyAppApi', 'Roles')
    Role_User = apps.get_model('MyAppApi', 'Role_User')
    Permissions = apps.get_model('MyAppApi', 'Permissions')
    Permission_User = apps.get_model('MyAppApi', 'Permission_User')

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

    user = User.objects.create(
        User_Number="USR0001",
        User_First_Name="Mohammed",
        User_Last_Name="Ennouaim",
        User_Role="Super Administrateur",
        User_Email="ennouaim@gestop.ma",
        User_Password="pbkdf2_sha256$600000$SzGGIMXtZfNz1rcry4eUfA$ruHqOsBErvhSQwdImVXHix0L+fDKp0sv3uq09AQa4qk=",
        User_Password_Crypt="b'O=V<7Zf-z0IR'",
        Group=group
    )

    role_sup = Role.objects.create(
        Role_Name="Super Admin",
        Role_Description="Super Administrateur role"
    )
    role_admin = Role.objects.create(
        Role_Name="Administrateur",
        Role_Description="Administrateur role"
    )
    role_mem = Role.objects.create(
        Role_Name="Member",
        Role_Description="Member role"
    )

    Role_User.objects.create(
        User=user,
        Role=role_sup
    )
    Role_User.objects.create(
        User=user,
        Role=role_admin
    )
    Role_User.objects.create(
        User=user,
        Role=role_mem
    )

    permission_add = Permissions.objects.create(
        Permission_Name="add",
        Permission_Description="Description Add"
    )
    permission_view = Permissions.objects.create(
        Permission_Name="view",
        Permission_Description="Description View"
    )
    permission_update = Permissions.objects.create(
        Permission_Name="update",
        Permission_Description="Description Update"
    )
    permission_delete = Permissions.objects.create(
        Permission_Name="delete",
        Permission_Description="Description Delete"
    )
    permission_sms = Permissions.objects.create(
        Permission_Name="sms",
        Permission_Description="Description sms"
    )
    permission_traceability = Permissions.objects.create(
        Permission_Name="traceability",
        Permission_Description="Description Traceability"
    )

    Permission_User.objects.create(
        User=user,
        Permission=permission_add
    )
    Permission_User.objects.create(
        User=user,
        Permission=permission_view
    )
    Permission_User.objects.create(
        User=user,
        Permission=permission_update
    )
    Permission_User.objects.create(
        User=user,
        Permission=permission_delete
    )
    Permission_User.objects.create(
        User=user,
        Permission=permission_sms
    )
    Permission_User.objects.create(
        User=user,
        Permission=permission_traceability
    )

class Migration(migrations.Migration):

    dependencies = [
        ('MyAppApi', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(insert_initial_data),
    ]
