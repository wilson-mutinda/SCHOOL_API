# Generated by Django 5.2 on 2025-04-17 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0028_cats_cat_term'),
    ]

    operations = [
        migrations.AddField(
            model_name='reportform',
            name='term_name',
            field=models.CharField(default=1, max_length=20, unique=True),
            preserve_default=False,
        ),
    ]
