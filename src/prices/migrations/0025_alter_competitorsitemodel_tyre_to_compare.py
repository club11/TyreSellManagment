# Generated by Django 4.0.6 on 2022-12-13 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prices', '0024_remove_competitorsitemodel_tyre_to_compare_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competitorsitemodel',
            name='tyre_to_compare',
            field=models.ManyToManyField(blank=True, related_name='price_tyre_to_compare', to='prices.comparativeanalysistyresmodel'),
        ),
    ]
