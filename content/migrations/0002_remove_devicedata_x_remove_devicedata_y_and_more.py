# Generated by Django 4.2 on 2024-05-29 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='devicedata',
            name='x',
        ),
        migrations.RemoveField(
            model_name='devicedata',
            name='y',
        ),
        migrations.AddField(
            model_name='devicedata',
            name='location',
            field=models.CharField(default='', max_length=250),
        ),
    ]