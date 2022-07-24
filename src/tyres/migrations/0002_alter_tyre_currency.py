# Generated by Django 4.0.6 on 2022-07-22 18:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dictionaries', '0001_initial'),
        ('tyres', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tyre',
            name='currency',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, related_name='tyre_currency', to='dictionaries.currency'),
        ),
    ]
