# Generated by Django 3.1.1 on 2020-12-03 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surfexif', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='images',
            field=models.ManyToManyField(blank=True, related_name='tags_with_image', to='surfexif.Image'),
        ),
        migrations.AlterUniqueTogether(
            name='tag',
            unique_together={('descriptor', 'category')},
        ),
    ]
