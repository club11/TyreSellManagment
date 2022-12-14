# Generated by Django 4.0.6 on 2022-12-15 19:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dictionaries', '0005_studdedusagemodel'),
        ('tyres', '0004_alter_tyreaddedfeaturemodel_season_usage'),
    ]

    operations = [
        migrations.AddField(
            model_name='tyreaddedfeaturemodel',
            name='studded_usage',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='competitor_studded_uusage', to='dictionaries.studdedusagemodel'),
        ),
        migrations.AlterField(
            model_name='tyreaddedfeaturemodel',
            name='season_usage',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='competitor_sseason_uusage', to='dictionaries.seasonusagemodel'),
        ),
    ]
