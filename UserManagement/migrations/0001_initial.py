# Generated by Django 4.0.4 on 2022-10-16 23:41

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='FacebookUser',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='UserManagement.user')),
                ('username', models.CharField(default='', max_length=255, unique=True)),
                ('profileId', models.CharField(default='', max_length=255, unique=True)),
                ('picture', models.CharField(default='', max_length=255, unique=True)),
            ],
            bases=('UserManagement.user', models.Model),
        ),
        migrations.CreateModel(
            name='GenericUser',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='UserManagement.user')),
                ('username', models.CharField(default='', max_length=255, unique=True)),
                ('email', models.CharField(default='', max_length=255, unique=True)),
                ('password', models.CharField(default='', max_length=255, unique=True)),
                ('salt', models.CharField(default='', max_length=255, unique=True)),
                ('tries', models.IntegerField(default=3)),
                ('blocked', models.BooleanField(default=False)),
                ('verified', models.BooleanField(default=False)),
                ('twoFactorAuth', models.BooleanField(default=False)),
            ],
            bases=('UserManagement.user', models.Model),
        ),
        migrations.CreateModel(
            name='GoogleUser',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='UserManagement.user')),
                ('username', models.CharField(default='', max_length=255, unique=True)),
                ('email', models.CharField(default='', max_length=255, unique=True)),
            ],
            bases=('UserManagement.user', models.Model),
        ),
        migrations.CreateModel(
            name='TwoFactorAuthCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(default='', max_length=255, unique=True)),
                ('expirationDate', models.DateTimeField(default=datetime.datetime(2022, 10, 16, 23, 46, 52, 33264))),
                ('user', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='UserManagement.user')),
            ],
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(default='', max_length=255, unique=True)),
                ('user', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='UserManagement.user')),
            ],
        ),
        migrations.CreateModel(
            name='PasswordResetCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(default='', max_length=255, unique=True)),
                ('expirationDate', models.DateTimeField(default=datetime.datetime(2022, 10, 16, 23, 46, 52, 32076))),
                ('user', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='UserManagement.user')),
            ],
        ),
        migrations.CreateModel(
            name='LocationCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(default='', max_length=255, unique=True)),
                ('expirationDate', models.DateTimeField(default=datetime.datetime(2022, 10, 16, 23, 46, 52, 34522))),
                ('user', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='UserManagement.user')),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(default='', max_length=255, unique=True)),
                ('user', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='UserManagement.user')),
            ],
        ),
        migrations.CreateModel(
            name='ConfirmationCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(default='', max_length=255, unique=True)),
                ('expirationDate', models.DateTimeField(default=datetime.datetime(2022, 10, 16, 23, 46, 52, 29253))),
                ('user', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='UserManagement.user')),
            ],
        ),
    ]