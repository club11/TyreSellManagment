# Generated by Django 4.0.6 on 2023-10-17 20:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tyres', '0001_initial'),
        ('dictionaries', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Belarus902PriceModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(blank=True, default=0, verbose_name='прейскуранты №№9, 902')),
                ('date_period', models.DateField(blank=True, verbose_name='период действия')),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='belarus902currency', to='dictionaries.currency')),
                ('tyre', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='belarus902price', to='tyres.tyre')),
            ],
        ),
        migrations.CreateModel(
            name='ChemCurierTyresModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tyre_size_chem', models.CharField(max_length=10, verbose_name='типоразмер химкурьер')),
                ('producer_chem', models.CharField(max_length=15, verbose_name='производитель химкурьер')),
                ('reciever_chem', models.CharField(blank=True, max_length=25, verbose_name='получатель химкурьер')),
                ('prod_country', models.CharField(blank=True, max_length=25, verbose_name='страна производства')),
                ('data_month_chem', models.DateField(blank=True, verbose_name='месяц (дата) поставки')),
                ('val_on_moth_chem', models.IntegerField(blank=True, null=True, verbose_name='объем поставки на дату(месяц) шт.')),
                ('money_on_moth_chem', models.FloatField(blank=True, max_length=20, null=True, verbose_name='объем поставки на дату(месяц) деньги')),
                ('average_price_in_usd', models.FloatField(blank=True, max_length=20, null=True, verbose_name='средневзвешеная цена, в USD')),
                ('currency_chem', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dictionaries.currency')),
                ('group_chem', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='chemcurier_group_uusage', to='dictionaries.tyregroupmodel', verbose_name='группа шин')),
            ],
        ),
        migrations.CreateModel(
            name='ComparativeAnalysisTableModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('market_table', models.CharField(blank=True, max_length=15, null=True, verbose_name='рынок сбыта')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='comparative_analysis_table', to=settings.AUTH_USER_MODEL, verbose_name='Таблица сравнительного анализа')),
            ],
        ),
        migrations.CreateModel(
            name='ComparativeAnalysisTyresModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sale_data', models.DateField(blank=True, null=True, verbose_name='Дата парсинга')),
                ('belarus902price', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='tyre_belarus902price', to='prices.belarus902pricemodel')),
            ],
        ),
        migrations.CreateModel(
            name='TPSRussiaFCAModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(blank=True, default=0, verbose_name='ТПС РФ FCA')),
                ('date_period', models.DateField(blank=True, verbose_name='период действия')),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tpsrussiafcacurrency', to='dictionaries.currency')),
                ('tyre', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tpsrussiafcaprice', to='tyres.tyre')),
            ],
        ),
        migrations.CreateModel(
            name='TPSMiddleAsiaFCAModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(blank=True, default=0, verbose_name='ТПС Средняя Азия, Закавказье, Молдова FCA')),
                ('date_period', models.DateField(blank=True, verbose_name='период действия')),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tpsmiddleasiafcacurrency', to='dictionaries.currency')),
                ('tyre', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tpsmiddleasiafcaprice', to='tyres.tyre')),
            ],
        ),
        migrations.CreateModel(
            name='TPSKazFCAModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(blank=True, default=0, verbose_name='ТПС Казахстан FCA')),
                ('date_period', models.DateField(blank=True, verbose_name='период действия')),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tpskazfcacurrency', to='dictionaries.currency')),
                ('tyre', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tpskazfcaprice', to='tyres.tyre')),
            ],
        ),
        migrations.CreateModel(
            name='SemiVariableCosstModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(blank=True, default=0, verbose_name='прямые затраты')),
                ('date_period', models.DateField(blank=True, verbose_name='период действия')),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='semi_variable_prices_currency', to='dictionaries.currency')),
                ('tyre', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='semi_variable_costs', to='tyres.tyre')),
            ],
        ),
        migrations.CreateModel(
            name='PlannedCosstModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(blank=True, default=0, verbose_name='плановая себестоимость')),
                ('date_period', models.DateField(blank=True, verbose_name='период действия')),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='prices_currency', to='dictionaries.currency')),
                ('tyre', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='planned_costs', to='tyres.tyre')),
            ],
        ),
        migrations.CreateModel(
            name='DataPriceValMoneyChemCurierModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_month_chem', models.DateTimeField(verbose_name='месяц (дата) поставки')),
                ('val_on_moth_chem', models.IntegerField(blank=True, null=True, verbose_name='объем поставки на дату(месяц) шт.')),
                ('money_on_moth_chem', models.FloatField(blank=True, max_length=20, null=True, verbose_name='объем поставки на дату(месяц) деньги')),
                ('price_on_date_chem', models.FloatField(blank=True, max_length=20, null=True, verbose_name='цена на дату(месяц) деньги')),
                ('price_val_money_data', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='price_val_money_data_obj', to='prices.chemcuriertyresmodel', verbose_name='цены, объемы продаж на дату')),
            ],
        ),
        migrations.CreateModel(
            name='CurrentPricesModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(blank=True, default=0, verbose_name='Действующие цены')),
                ('date_period', models.DateField(blank=True, verbose_name='период действия')),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='currentpricescurrency', to='dictionaries.currency')),
                ('tyre', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='currentpricesprice', to='tyres.tyre')),
            ],
        ),
        migrations.CreateModel(
            name='CompetitorSiteModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site', models.CharField(blank=True, max_length=30, null=True, verbose_name='наименование сайта')),
                ('price', models.FloatField(blank=True, null=True, verbose_name='цена конкурента')),
                ('date_period', models.DateField(blank=True, verbose_name='период действия')),
                ('tyresize_competitor', models.CharField(blank=True, max_length=25, verbose_name='типоразмер конкурент')),
                ('name_competitor', models.CharField(blank=True, max_length=25, verbose_name='наименование конкурент')),
                ('parametres_competitor', models.CharField(blank=True, max_length=25, verbose_name='параметры конкурент')),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dictionaries.currency')),
                ('developer', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='developer_competitor', to='dictionaries.competitormodel')),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='competitor_site_group_uusage', to='dictionaries.tyregroupmodel', verbose_name='группа шин')),
                ('season', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='competitor_site_sseason_uusage', to='dictionaries.seasonusagemodel', verbose_name='сезонность')),
                ('tyre_to_compare', models.ManyToManyField(blank=True, related_name='price_tyre_to_compare', to='prices.comparativeanalysistyresmodel')),
            ],
        ),
        migrations.AddField(
            model_name='comparativeanalysistyresmodel',
            name='currentpricesprice',
            field=models.ForeignKey(blank=True, default=0, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='tyre_currentpricesprice', to='prices.currentpricesmodel'),
        ),
        migrations.AddField(
            model_name='comparativeanalysistyresmodel',
            name='planned_costs',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='tyre_planned_costs', to='prices.plannedcosstmodel'),
        ),
        migrations.AddField(
            model_name='comparativeanalysistyresmodel',
            name='semi_variable_prices',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='tyre_semi_variable_prices', to='prices.semivariablecosstmodel'),
        ),
        migrations.AddField(
            model_name='comparativeanalysistyresmodel',
            name='table',
            field=models.ManyToManyField(blank=True, related_name='comparative_table', to='prices.comparativeanalysistablemodel', verbose_name='Таблица'),
        ),
        migrations.AddField(
            model_name='comparativeanalysistyresmodel',
            name='tpskazfcaprice',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='tyre_tpskazfcaprice', to='prices.tpskazfcamodel'),
        ),
        migrations.AddField(
            model_name='comparativeanalysistyresmodel',
            name='tpsmiddleasiafcaprice',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='tyre_tpsmiddleasiafcaprice', to='prices.tpsmiddleasiafcamodel'),
        ),
        migrations.AddField(
            model_name='comparativeanalysistyresmodel',
            name='tpsrussiafcaprice',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='tyre_tpsrussiafcaprice', to='prices.tpsrussiafcamodel'),
        ),
        migrations.AddField(
            model_name='comparativeanalysistyresmodel',
            name='tyre',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tyre_comparative', to='tyres.tyre'),
        ),
    ]
