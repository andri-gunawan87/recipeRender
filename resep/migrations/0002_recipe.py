# Generated by Django 3.2.1 on 2021-05-26 06:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('resep', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('key', models.CharField(max_length=64)),
                ('image', models.URLField()),
                ('difficulty', models.CharField(max_length=64)),
                ('times', models.CharField(max_length=64)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('desc', models.CharField(max_length=200)),
                ('ingredient', models.JSONField()),
                ('step', models.JSONField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
