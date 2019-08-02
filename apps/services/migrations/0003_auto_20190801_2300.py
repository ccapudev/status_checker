# Generated by Django 2.2.4 on 2019-08-01 23:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0002_auto_20190801_2058'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkpoint',
            name='headers',
            field=models.TextField(blank=True, null=True, verbose_name='Cabeceras'),
        ),
        migrations.AddField(
            model_name='checkpoint',
            name='reason',
            field=models.IntegerField(blank=True, null=True, verbose_name='Razon de estado'),
        ),
        migrations.AddField(
            model_name='checkpoint',
            name='response_time',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=9, verbose_name='Tiempo de repuesta'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='checkpoint',
            name='web_service',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='checkpoints', to='services.WebService'),
        ),
        migrations.CreateModel(
            name='CheckpointErrors',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(blank=True, max_length=200, null=True, verbose_name='Razon')),
                ('traceback_log', models.TextField(blank=True, null=True, verbose_name='Traceback')),
                ('web_service', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='checkpoints_errors', to='services.WebService')),
            ],
        ),
    ]