# Generated by Django 4.1.4 on 2022-12-08 01:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('closet', '0002_alter_color_mapping'),
    ]

    operations = [
        migrations.AddField(
            model_name='clothes',
            name='url',
            field=models.CharField(default='', max_length=100),
        ),
    ]
