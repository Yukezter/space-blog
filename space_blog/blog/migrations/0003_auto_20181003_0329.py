# Generated by Django 2.0.8 on 2018-10-03 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20181003_0252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpage',
            name='category',
            field=models.CharField(choices=[('Technology', 'Technology'), ('Missions', 'Missions'), ('Politics', 'Politics'), ('Discoveries', 'Discoveries')], max_length=256),
        ),
    ]
