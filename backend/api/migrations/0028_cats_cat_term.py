# Generated by Django 5.2 on 2025-04-17 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0027_term'),
    ]

    operations = [
        migrations.AddField(
            model_name='cats',
            name='cat_term',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
    ]
