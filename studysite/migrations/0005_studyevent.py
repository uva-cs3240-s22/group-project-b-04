# Generated by Django 4.0.2 on 2022-04-10 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studysite', '0004_friendrequest'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudyEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max_users', models.IntegerField(default=6)),
                ('course', models.ManyToManyField(blank=True, to='studysite.Course')),
                ('users', models.ManyToManyField(to='studysite.UserProfile')),
            ],
        ),
    ]