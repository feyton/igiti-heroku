# Generated by Django 4.0.4 on 2022-05-21 18:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blogpost',
            old_name='text',
            new_name='content',
        ),
        migrations.RemoveField(
            model_name='blogpost',
            name='description',
        ),
    ]
