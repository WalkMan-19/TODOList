# Generated by Django 4.1.6 on 2023-02-25 07:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tguser',
            options={'verbose_name': 'Телеграм пользователь', 'verbose_name_plural': 'Телеграм пользователи'},
        ),
    ]