# Generated by Django 3.2.13 on 2022-05-22 22:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0002_sitesettings'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SiteSettings',
            new_name='Settings',
        ),
    ]