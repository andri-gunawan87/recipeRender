# Generated by Django 3.2.1 on 2021-06-26 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resep', '0007_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='key',
            field=models.CharField(max_length=128),
        ),
    ]
