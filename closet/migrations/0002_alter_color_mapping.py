# Generated by Django 4.1.4 on 2022-12-07 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('closet', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='color',
            name='mapping',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]