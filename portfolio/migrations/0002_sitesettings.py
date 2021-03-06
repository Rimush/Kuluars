# Generated by Django 3.2.13 on 2022-05-22 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_url', models.URLField(max_length=256, verbose_name='Website url')),
                ('title', models.CharField(max_length=256, verbose_name='Title')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
