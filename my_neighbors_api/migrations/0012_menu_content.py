# Generated by Django 3.1.7 on 2021-03-24 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_neighbors_api', '0011_auto_20210324_0229'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='content',
            field=models.TextField(blank=True, null=True),
        ),
    ]
