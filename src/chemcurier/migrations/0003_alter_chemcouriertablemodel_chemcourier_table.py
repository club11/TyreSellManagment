# Generated by Django 4.0.6 on 2024-05-22 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chemcurier', '0002_chemcouriertablemodel_chemurier_in_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chemcouriertablemodel',
            name='chemcourier_table',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Хим Курьер'),
        ),
    ]
