# Generated by Django 4.0.6 on 2024-05-22 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tyres', '0002_alter_tyreaddedfeaturemodel_ax_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tyreaddedfeaturemodel',
            name='tyre_thread',
            field=models.CharField(max_length=40, null=True, verbose_name='рисунок протектора'),
        ),
    ]
