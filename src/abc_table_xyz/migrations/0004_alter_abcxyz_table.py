# Generated by Django 4.0.6 on 2022-08-18 17:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('abc_table_xyz', '0003_abcxyz_tyre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='abcxyz',
            name='table',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='table', to='abc_table_xyz.abcxyztable', verbose_name='Таблица'),
        ),
    ]
