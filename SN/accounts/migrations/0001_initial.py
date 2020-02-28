# Generated by Django 3.0.3 on 2020-02-27 18:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import sn_mixins.functions


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True, max_length=500)),
                ('location', models.CharField(blank=True, max_length=30)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('slug', models.SlugField(unique=True)),
                ('image', models.ImageField(blank=True, height_field='height_field', null=True, upload_to=sn_mixins.functions.upload_location, width_field='width_field')),
                ('height_field', models.IntegerField(default=0)),
                ('width_field', models.IntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-user__date_joined'],
            },
        ),
    ]