# Generated by Django 2.2.13 on 2022-06-22 18:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='neighbourhood',
            new_name='city',
        ),
    ]
