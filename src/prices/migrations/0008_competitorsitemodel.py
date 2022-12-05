# Generated by Django 4.0.6 on 2022-11-21 18:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dictionaries', '0001_initial'),
        ('tyres', '0001_initial'),
        ('prices', '0007_alter_comparativeanalysistyresmodel_currentpricesprice'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompetitorSiteModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(blank=True, verbose_name='цена конкурента')),
                ('date_period', models.DateField(blank=True, verbose_name='период действия')),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dictionaries.currency')),
                ('tyre', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='competitortyre', to='tyres.tyre')),
            ],
        ),
    ]
