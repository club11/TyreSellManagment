# Generated by Django 4.0.6 on 2022-10-30 08:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tyres', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('prices', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ComparativeAnalysisTableModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='comparative_analysis_table', to=settings.AUTH_USER_MODEL, verbose_name='Таблица сравнительного анализа')),
            ],
        ),
        migrations.CreateModel(
            name='ComparativeAnalysisTyresModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('belarus902price', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tyre_belarus902price', to='prices.belarus902pricemodel')),
                ('planned_costs', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tyre_planned_costs', to='prices.plannedcosstmodel')),
                ('semi_variable_prices', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tyre_semi_variable_prices', to='prices.semivariablecosstmodel')),
                ('table', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comparative_table', to='prices.comparativeanalysistablemodel', verbose_name='Таблица')),
                ('tpskazfcaprice', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tyre_tpskazfcaprice', to='prices.tpskazfcamodel')),
                ('tpsmiddleasiafcaprice', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tyre_tpsmiddleasiafcaprice', to='prices.tpsmiddleasiafcamodel')),
                ('tpsrussiafcaprice', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tyre_tpsrussiafcaprice', to='prices.tpsrussiafcamodel')),
                ('tyre', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tyre_comparative', to='tyres.tyre')),
            ],
        ),
    ]
