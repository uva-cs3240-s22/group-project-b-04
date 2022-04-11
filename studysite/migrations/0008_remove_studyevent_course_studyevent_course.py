# Generated by Django 4.0.2 on 2022-04-11 06:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('studysite', '0007_studyevent_description_studyevent_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studyevent',
            name='course',
        ),
        migrations.AddField(
            model_name='studyevent',
            name='course',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='studysite.course'),
        ),
    ]
