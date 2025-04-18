# Generated by Django 5.2 on 2025-04-16 11:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0025_alter_catandexamgrading_student_subject'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReportForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_code', models.CharField(max_length=200)),
                ('student_first_name', models.CharField(max_length=200)),
                ('student_last_name', models.CharField(max_length=200)),
                ('student_class', models.CharField(max_length=10)),
                ('student_stream', models.CharField(max_length=10)),
                ('student_average_grade', models.CharField(max_length=10)),
                ('teacher_remarks', models.TextField()),
                ('total_subjects', models.IntegerField()),
                ('total_marks', models.IntegerField()),
                ('is_english_cat', models.IntegerField(default=0)),
                ('is_english_exam', models.IntegerField(default=0)),
                ('is_english_total', models.IntegerField(default=0)),
                ('is_english_grade', models.CharField(default=0)),
                ('is_maths_cat', models.IntegerField(default=0)),
                ('is_maths_exam', models.IntegerField(default=0)),
                ('is_maths_total', models.IntegerField(default=0)),
                ('is_maths_grade', models.CharField(default=0)),
                ('is_kiswahili_cat', models.IntegerField(default=0)),
                ('is_kiswahili_exam', models.IntegerField(default=0)),
                ('is_kiswahili_total', models.IntegerField(default=0)),
                ('is_kiswahili_grade', models.CharField(default=0)),
                ('is_physics_cat', models.IntegerField(default=0)),
                ('is_physics_exam', models.IntegerField(default=0)),
                ('is_physics_total', models.IntegerField(default=0)),
                ('is_physics_grade', models.CharField(default=0)),
                ('is_chemistry_cat', models.IntegerField(default=0)),
                ('is_chemistry_exam', models.IntegerField(default=0)),
                ('is_chemistry_total', models.IntegerField(default=0)),
                ('is_chemistry_grade', models.CharField(default=0)),
                ('is_biology_cat', models.IntegerField(default=0)),
                ('is_biology_exam', models.IntegerField(default=0)),
                ('is_biology_total', models.IntegerField(default=0)),
                ('is_biology_grade', models.CharField(default=0)),
                ('is_geography_cat', models.IntegerField(default=0)),
                ('is_geography_exam', models.IntegerField(default=0)),
                ('is_geography_total', models.IntegerField(default=0)),
                ('is_geography_grade', models.CharField(default=0)),
                ('is_cre_cat', models.IntegerField(default=0)),
                ('is_cre_exam', models.IntegerField(default=0)),
                ('is_cre_total', models.IntegerField(default=0)),
                ('is_cre_grade', models.CharField(default=0)),
                ('is_history_cat', models.IntegerField(default=0)),
                ('is_history_exam', models.IntegerField(default=0)),
                ('is_history_total', models.IntegerField(default=0)),
                ('is_history_grade', models.CharField(default=0)),
                ('is_agriculture_cat', models.IntegerField(default=0)),
                ('is_agriculture_exam', models.IntegerField(default=0)),
                ('is_agriculture_total', models.IntegerField(default=0)),
                ('is_agriculture_grade', models.CharField(default=0)),
                ('is_computer_studies_cat', models.IntegerField(default=0)),
                ('is_computer_studies_exam', models.IntegerField(default=0)),
                ('is_computer_studies_total', models.IntegerField(default=0)),
                ('is_computer_studies_grade', models.CharField(default=0)),
                ('is_business_studies_cat', models.IntegerField(default=0)),
                ('is_business_studies_exam', models.IntegerField(default=0)),
                ('is_business_studies_total', models.IntegerField(default=0)),
                ('is_business_studies_grade', models.CharField(default=0)),
                ('class_teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='report_forms', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
