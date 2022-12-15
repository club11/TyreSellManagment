# Generated by Django 4.0.6 on 2022-12-13 18:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tyres', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TyreAddedFeatureModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('indexes_list', models.CharField(max_length=30, verbose_name='список индексов')),
                ('season_usage', models.CharField(max_length=15, verbose_name='сезонность')),
                ('tyre_thread', models.CharField(max_length=15, verbose_name='рисунок протектора')),
                ('ax', models.CharField(max_length=15, verbose_name='ось')),
                ('usability', models.CharField(max_length=15, verbose_name='применяемость')),
                ('tyre', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='added_features', to='tyres.tyre', verbose_name='дополнительные данные о шине')),
            ],
        ),
    ]
