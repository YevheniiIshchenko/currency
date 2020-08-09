# Generated by Django 2.2.12 on 2020-08-06 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rate', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rate',
            name='source',
            field=models.PositiveSmallIntegerField(choices=[(1, 'PrivateBank'), (2, 'MonoBank'), (3, 'VKurse.dp.ua'), (4, 'Raiffeisen Bank'), (5, 'Alpha-Bank'), (6, 'Black Market')]),
        ),
    ]