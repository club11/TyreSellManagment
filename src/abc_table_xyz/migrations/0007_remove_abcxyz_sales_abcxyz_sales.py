# Generated by Django 4.0.6 on 2022-08-18 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0001_initial'),
        ('abc_table_xyz', '0006_remove_abcxyz_sales_abcxyz_sales'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='abcxyz',
            name='sales',
        ),
        migrations.AddField(
            model_name='abcxyz',
            name='sales',
            field=models.ManyToManyField(blank=True, null=True, related_name='sales_data', to='sales.sales', verbose_name='продажи'),
        ),
    ]
