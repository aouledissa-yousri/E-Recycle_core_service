# Generated by Django 4.0.4 on 2022-10-16 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='citizen',
            name='lastname',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='citizen',
            name='name',
            field=models.CharField(default='', max_length=255),
        ),
    ]