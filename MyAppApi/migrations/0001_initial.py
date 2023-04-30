# Generated by Django 4.1.7 on 2023-04-30 00:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Directory',
            fields=[
                ('Directory_Id', models.AutoField(primary_key=True, serialize=False)),
                ('Directory_Name', models.CharField(max_length=500)),
                ('Directory_Description', models.CharField(max_length=500)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_by', models.IntegerField(default=None, null=True)),
                ('deleted_at', models.DateTimeField(default=None, null=True)),
            ],
            options={
                'db_table': 'directory',
            },
        ),
        migrations.CreateModel(
            name='Entities',
            fields=[
                ('Entity_Id', models.AutoField(primary_key=True, serialize=False)),
                ('Entity_Number', models.CharField(max_length=500)),
                ('Entity_Name', models.CharField(max_length=500)),
                ('Entity_Description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_by', models.IntegerField(default=None, null=True)),
                ('deleted_at', models.DateTimeField(default=None, null=True)),
            ],
            options={
                'db_table': 'entities',
            },
        ),
        migrations.CreateModel(
            name='Groups',
            fields=[
                ('Group_Id', models.AutoField(primary_key=True, serialize=False)),
                ('Group_Number', models.CharField(max_length=500)),
                ('Group_Name', models.CharField(max_length=500)),
                ('Group_Description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_by', models.IntegerField(default=None, null=True)),
                ('deleted_at', models.DateTimeField(default=None, null=True)),
                ('Entity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MyAppApi.entities')),
            ],
            options={
                'db_table': 'groups',
            },
        ),
        migrations.CreateModel(
            name='Mailing_List',
            fields=[
                ('Mailing_List_Id', models.AutoField(primary_key=True, serialize=False)),
                ('Mailing_List_Name', models.CharField(max_length=500)),
                ('Mailing_List_Url', models.CharField(max_length=500)),
                ('Mailing_List_File', models.FileField(upload_to='Mailing List/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_by', models.IntegerField(default=None, null=True)),
                ('deleted_at', models.DateTimeField(default=None, null=True)),
            ],
            options={
                'db_table': 'mailing_list',
            },
        ),
        migrations.CreateModel(
            name='Number_List',
            fields=[
                ('Number_Id', models.AutoField(primary_key=True, serialize=False)),
                ('Number_Name', models.CharField(max_length=500)),
                ('Number', models.CharField(max_length=500)),
                ('Number_Email', models.CharField(max_length=500)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_by', models.IntegerField(default=None, null=True)),
                ('deleted_at', models.DateTimeField(default=None, null=True)),
            ],
            options={
                'db_table': 'number_list',
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('User_Id', models.AutoField(primary_key=True, serialize=False)),
                ('User_Number', models.CharField(max_length=500)),
                ('User_First_Name', models.CharField(max_length=500)),
                ('User_Last_Name', models.CharField(max_length=500)),
                ('User_Role', models.CharField(max_length=500)),
                ('User_Email', models.CharField(max_length=500)),
                ('User_Password', models.CharField(max_length=500)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_by', models.IntegerField(default=None, null=True)),
                ('deleted_at', models.DateTimeField(default=None, null=True)),
                ('Group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MyAppApi.groups')),
            ],
            options={
                'db_table': 'users',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('Message_Id', models.AutoField(primary_key=True, serialize=False)),
                ('Message_Name', models.CharField(max_length=500)),
                ('Message_Text', models.CharField(max_length=500)),
                ('Message_Language', models.CharField(max_length=500)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_by', models.IntegerField(default=None, null=True)),
                ('deleted_at', models.DateTimeField(default=None, null=True)),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MyAppApi.users')),
            ],
            options={
                'db_table': 'message',
            },
        ),
        migrations.CreateModel(
            name='Log_Message',
            fields=[
                ('Id', models.AutoField(primary_key=True, serialize=False)),
                ('Recipient', models.CharField(max_length=500)),
                ('Modem', models.CharField(max_length=500)),
                ('Message', models.CharField(max_length=500)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_by', models.IntegerField(default=None, null=True)),
                ('deleted_at', models.DateTimeField(default=None, null=True)),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MyAppApi.users')),
            ],
            options={
                'db_table': 'log_message',
            },
        ),
        migrations.CreateModel(
            name='Log_App',
            fields=[
                ('Id', models.AutoField(primary_key=True, serialize=False)),
                ('Operation', models.CharField(max_length=500)),
                ('Table', models.CharField(max_length=500)),
                ('Object', models.CharField(max_length=500)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_by', models.IntegerField(default=None, null=True)),
                ('deleted_at', models.DateTimeField(default=None, null=True)),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MyAppApi.users')),
            ],
            options={
                'db_table': 'log_app',
            },
        ),
        migrations.CreateModel(
            name='Directory_Number',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Directory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MyAppApi.directory')),
                ('Number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MyAppApi.number_list')),
            ],
            options={
                'db_table': 'directory_number',
                'unique_together': {('Directory', 'Number')},
            },
        ),
    ]
