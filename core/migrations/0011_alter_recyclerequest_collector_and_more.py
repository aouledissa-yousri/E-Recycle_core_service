# Generated by Django 4.1.2 on 2022-10-30 13:16

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_collector_lastname_collector_name_collector_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recyclerequest',
            name='Collector',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.collector'),
        ),
        migrations.AlterField(
            model_name='recyclerequest',
            name='dateSubmitted',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 30, 13, 16, 22, 493151, tzinfo=datetime.timezone.utc)),
        ),
    ]
