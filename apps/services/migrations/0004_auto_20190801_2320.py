# Generated by Django 2.2.4 on 2019-08-01 23:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0003_auto_20190801_2300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkpoint',
            name='reason',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='Razon de estado'),
        ),
    ]
