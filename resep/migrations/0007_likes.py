# Generated by Django 3.2.1 on 2021-06-09 04:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('resep', '0006_alter_recipe_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='Likes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like', models.BooleanField(default=False)),
                ('dislike', models.BooleanField(default=False)),
                ('rec', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='like', to='resep.recipe')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_like', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
