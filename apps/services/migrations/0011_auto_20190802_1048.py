# Generated by Django 2.2.4 on 2019-08-02 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0010_webservice_slack_api'),
    ]

    operations = [
        migrations.AlterField(
            model_name='webservice',
            name='minutes',
            field=models.PositiveIntegerField(default=2, verbose_name='Intervalo en minutos'),
        ),
        migrations.AlterField(
            model_name='webservice',
            name='slack_api',
            field=models.URLField(blank=True, null=True, verbose_name='Slack Webhook URL'),
        ),
    ]
