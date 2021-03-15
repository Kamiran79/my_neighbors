# Generated by Django 3.1.7 on 2021-03-15 00:00

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('my_neighbors_api', '0003_menurating_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChefRating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('my_user_chef', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='my_neighbors_api.myneighborsuser')),
                ('my_user_user', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'rating',
                'verbose_name_plural': 'ratings',
            },
        ),
    ]
