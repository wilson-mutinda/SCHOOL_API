# Generated by Django 5.2 on 2025-04-11 01:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_alter_catandexam_student_cat_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='StreamClassSubjects',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_code', models.CharField(max_length=20, unique=True)),
                ('student_class', models.CharField(max_length=10)),
                ('student_stream', models.CharField(max_length=10)),
                ('subject_count', models.IntegerField()),
                ('is_english', models.BooleanField(default=True)),
                ('is_maths', models.BooleanField(default=True)),
                ('is_kiswahili', models.BooleanField(default=True)),
                ('is_chemistry', models.BooleanField(default=True)),
                ('is_physics', models.BooleanField(default=True)),
                ('is_biology', models.BooleanField(default=True)),
                ('is_geography', models.BooleanField(default=True)),
                ('is_cre', models.BooleanField(default=True)),
                ('is_history', models.BooleanField(default=True)),
                ('is_computer_studies', models.BooleanField(default=True)),
                ('is_business_studies', models.BooleanField(default=True)),
                ('is_agriculture', models.BooleanField(default=True)),
                ('student_teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stream_class_subject', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
