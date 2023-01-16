# Generated by Django 4.0.6 on 2023-01-10 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prices', '0029_datapricevalmoneychemcuriermodel_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datapricevalmoneychemcuriermodel',
            name='money_on_moth_chem',
            field=models.FloatField(blank=True, max_length=20, null=True, verbose_name='объем поставки на дату(месяц) деньги'),
        ),
        migrations.AlterField(
            model_name='datapricevalmoneychemcuriermodel',
            name='price_on_date_chem',
            field=models.FloatField(blank=True, max_length=20, null=True, verbose_name='цена на дату(месяц) деньги'),
        ),
        migrations.AlterField(
            model_name='datapricevalmoneychemcuriermodel',
            name='val_on_moth_chem',
            field=models.IntegerField(blank=True, null=True, verbose_name='объем поставки на дату(месяц) шт.'),
        ),
    ]