# Generated by Django 5.2 on 2025-04-08 03:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_catresults'),
    ]

    operations = [
        migrations.CreateModel(
            name='CatGrading',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cat_marks', models.IntegerField()),
                ('cat_grade', models.CharField(blank=True, max_length=10, null=True)),
                ('is_english', models.BooleanField(default=False)),
                ('is_maths', models.BooleanField(default=False)),
                ('is_kiswahili', models.BooleanField(default=False)),
                ('is_chemistry', models.BooleanField(default=False)),
                ('is_physics', models.BooleanField(default=False)),
                ('is_biology', models.BooleanField(default=False)),
                ('is_history', models.BooleanField(default=False)),
                ('is_geography', models.BooleanField(default=False)),
                ('is_cre', models.BooleanField(default=False)),
                ('is_busines_studies', models.BooleanField(default=False)),
                ('is_agriculture', models.BooleanField(default=False)),
                ('is_computer_studies', models.BooleanField(default=False)),
                ('cat_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cat_grading', to='api.cat')),
                ('cat_student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cat_grading', to='api.student')),
                ('cat_subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cat_grading', to='api.subject')),
                ('cat_teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grading', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
