# Generated by Django 5.2 on 2025-04-09 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_alter_catgrading_marks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stream',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
