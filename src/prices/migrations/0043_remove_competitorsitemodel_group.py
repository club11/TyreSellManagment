# Generated by Django 4.0.6 on 2023-10-04 20:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prices', '0042_remove_competitorsitemodel_group_usage_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='competitorsitemodel',
            name='group',
        ),
    ]