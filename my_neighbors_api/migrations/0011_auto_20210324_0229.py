# Generated by Django 3.1.7 on 2021-03-24 02:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_neighbors_api', '0010_auto_20210324_0156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='foodImgUrl',
            field=models.ImageField(blank=True, null=True, upload_to='menus/'),
        ),
    ]
