# Generated by Django 4.0.6 on 2022-11-09 18:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('prices', '0006_comparativeanalysistyresmodel_currentpricesprice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comparativeanalysistyresmodel',
            name='currentpricesprice',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='tyre_currentpricesprice', to='prices.currentpricesmodel'),
        ),
    ]
