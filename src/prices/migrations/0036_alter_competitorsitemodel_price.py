# Generated by Django 4.0.6 on 2023-01-12 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prices', '0035_remove_chemcuriertyresmodel_price_val_money_data_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competitorsitemodel',
            name='price',
            field=models.FloatField(blank=True, null=True, verbose_name='цена конкурента'),
        ),
    ]
