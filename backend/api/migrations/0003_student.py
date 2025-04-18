# Generated by Django 5.2 on 2025-04-05 01:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_parent_parent_code_teacher_teacher_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parent_code', models.CharField(max_length=100, unique=True)),
                ('parent_email', models.EmailField(max_length=254, unique=True)),
                ('student_code', models.CharField(max_length=100, unique=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='students', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
