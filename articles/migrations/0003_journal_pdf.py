# Generated by Django 3.2.13 on 2022-05-11 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_auto_20220505_0648'),
    ]

    operations = [
        migrations.AddField(
            model_name='journal',
            name='pdf',
            field=models.FileField(default=1, upload_to='pdf/'),
            preserve_default=False,
        ),
    ]
