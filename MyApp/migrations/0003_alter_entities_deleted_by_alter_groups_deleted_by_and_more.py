# Generated by Django 4.2 on 2023-04-23 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyApp', '0002_entities_deleted_at_entities_deleted_by_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entities',
            name='deleted_by',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='groups',
            name='deleted_by',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='deleted_by',
            field=models.IntegerField(null=True),
        ),
    ]
