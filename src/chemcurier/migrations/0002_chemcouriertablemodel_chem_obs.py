# Generated by Django 4.0.6 on 2023-10-16 14:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('prices', '0057_chemcuriertyresmodel_prod_country'),
        ('chemcurier', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chemcouriertablemodel',
            name='chem_obs',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='chemcurier_tabe', to='prices.chemcuriertyresmodel', verbose_name='объект Хим курьер'),
        ),
    ]
