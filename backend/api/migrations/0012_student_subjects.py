# Generated by Django 5.2 on 2025-04-08 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_catandexamgrading'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='subjects',
            field=models.ManyToManyField(related_name='students', to='api.subject'),
        ),
    ]
