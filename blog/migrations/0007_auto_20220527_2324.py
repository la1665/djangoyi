# Generated by Django 2.2.5 on 2022-05-27 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20220521_1535'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='is_special',
            field=models.BooleanField(default=False, verbose_name='مقاله ویژه'),
        ),
    ]
