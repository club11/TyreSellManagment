# Generated by Django 4.0.6 on 2023-10-15 15:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dictionaries', '0005_studdedusagemodel'),
        ('prices', '0053_remove_chemcuriertyresmodel_group_chem_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chemcuriertyresmodel',
            name='roup_chem',
        ),
        migrations.AddField(
            model_name='chemcuriertyresmodel',
            name='group_chem',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='chemcurier_group_uusage', to='dictionaries.tyregroupmodel', verbose_name='группа шин'),
        ),
    ]