# Generated by Django 3.1.1 on 2020-12-03 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surfexif', '0002_auto_20201203_1800'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='descriptor',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterUniqueTogether(
            name='tag',
            unique_together=set(),
        ),
    ]