# Generated by Django 3.2.13 on 2022-05-12 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0005_auto_20220512_1241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journal',
            name='index',
            field=models.PositiveIntegerField(default=4, verbose_name='Порядковый номер'),
        ),
    ]
