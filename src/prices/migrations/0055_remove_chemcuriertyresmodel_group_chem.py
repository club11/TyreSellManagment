# Generated by Django 4.0.6 on 2023-10-15 15:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prices', '0054_remove_chemcuriertyresmodel_roup_chem_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chemcuriertyresmodel',
            name='group_chem',
        ),
    ]