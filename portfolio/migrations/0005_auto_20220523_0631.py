# Generated by Django 3.2.13 on 2022-05-22 22:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0004_polygraphy_work_in_elections'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='polygraphy',
            options={'verbose_name': 'полиграфию', 'verbose_name_plural': 'Полиграфия'},
        ),
        migrations.AlterModelOptions(
            name='video_products',
            options={'verbose_name': 'видео продукцию', 'verbose_name_plural': 'Видео продукция'},
        ),
        migrations.AlterModelOptions(
            name='work_in_elections',
            options={'verbose_name': 'работу на выборах', 'verbose_name_plural': 'Работа на выборах'},
        ),
    ]
