
def main():
    import datetime
    from prices import views
    from prices import models as prices_models

    def run_the_parscin_script():

        get_year  = datetime.datetime.now().year
        get_month  = datetime.datetime.now().month
        get_day  = datetime.datetime.now().day

        start = datetime.datetime(get_year, get_month, get_day, 23, 58) # !!!!!!! для введения часа и мин ля запуска скрипта
        delta = datetime.timedelta(minutes=0)
        end = start + delta
        end_hour = end.hour
        end_minute = end.minute
        end_execution = start + datetime.timedelta(minutes=2)
        #print('end_hour', end_hour, 'end_minute', end_minute)
        couple_min_checking = datetime.timedelta(minutes=1)
        get_current_time = datetime.datetime.now()
        minutes_to_start_left =  start - get_current_time 
        #print('!!!', minutes_to_start_left)
        #if minutes_to_start_left < couple_min_checking: # если до времени запуска скрипта осталось менее минуты - то начать
            #while True:
            ##    print(datetime.datetime.now())
            #    current_time = datetime.datetime.now()
            #    if current_time.hour == end_hour and current_time.minute == end_minute:    
            #        belarus_sites_parsing()
            #        break
            #    elif current_time.hour == end_execution.hour and current_time.minute == end_execution.minute:  
            #        break
    
        if get_current_time < start:
            prices_models.SCRIPT_IS_RUNNING = True
            views.running_programm() 
            print('END OF PARSING')    
        prices_models.SCRIPT_IS_RUNNING = False # вернуть в состояние по окончании действия скрипта
        print('PROFECY IS FULLFILLED !!!!! OMENS IN THE SKY')
        return 'the programm is fullfilled'
    

    #def sdfsdfsdsdf():
    #    import re
    #    goods_dict = {}
    #    reg_list = [
    #    #'\d{3}/\d{2}[A-Za-z]\d{2}(\(\d{2}(\.|\,)\d{1}[A-Za-z]\d{2}| \(\d{2}(\.|\,)\d{1}[A-Za-z]\d{2})', 
    #    #'\d{2}(\.|\,)(\d{2}|\d{1})(R|-)\d{2}', 
    #    #'(\d{3}|\d{2})/\d{2}([A-Za-z]|-)(\d{2}(\.|\,)\d{1}|\d{2}[A-Za-z]|\d{2})',  # = '(\d{3}|\d{2})/\d{2}([A-Za-z]|-)\d{2}' +  '\d{3}/\d{2}([A-Za-z]|-)(\d{2}(\.|\,)\d{1}|\d{2})',    
    #    '(\d{3}/\d{2}[A-Za-z]\d{2}(\(\d{2}(\.|\,)\d{1}[A-Za-z]\d{2}| \(\d{2}(\.|\,)\d{1}[A-Za-z]\d{2}))|(\d{2}(\.|\,)(\d{2}|\d{1})(R|-)\d{2})|((\d{3}|\d{2})/\d{2}([A-Za-z]|-)(\d{2}(\.|\,)\d{1}|\d{2}[A-Za-z]|\d{2}))', #3 в одном чтобы избежать повторений двойных в ячейке наподобие #АШ 480/80R42(18.4R42)
    #    '\d{2}(\.|\,)\d{1}[A-Za-z](R|-)\d{2}',
    #    '(\d{4}|\d{3})[A-Za-z]\d{3}([A-Za-z]|-)\d{3}',
    #    '\d{2}[A-Za-z]\d{1}([A-Za-z]|-)\d{1}',
    #    '\d{2}[A-Za-z]\d{1}(\.|\,)\d{2}([A-Za-z]|-)\d{1}',
    #    '\d{2}(\.|\,)\d{1}/\d{2}([A-Za-z]|-)(\d{2}(\.|\,)\d{1}|\d{2})',                       
    #    '\d{1}(\.|\,)\d{2}(([A-Za-z]|-)|[A-Za-z]-)\d{2}',
    #    '\d{1}[A-Za-z]-\d{2} ',
    #    '\d{3}[A-Za-z]\d{2}[A-Za-z]',
    #    '\s\d{2}([A-Za-z]|-)\d{2}(\.|\,)\d{1}', 
    #    '\d{2}[A-Za-z][A-Za-z]\d{2}', 
    #    ]
    #    list_to_check = ['автобусов и грузовых автомобилей', 'большегрузных автомобилей', 'строительной и дорожной техники', 'тракторов и сельскохозяйственной техники', 'микроавтобусов и легкогрузовых автомобилей']
    #    shins_phrase = ['шины', 'Шины']    
    #    from selenium import webdriver
    #    from bs4 import BeautifulSoup
    #    chrome_options = webdriver.ChromeOptions()
    #    chrome_options.add_argument("--no-sandbox")
    #    chrome_options.add_argument("--headless")
    #    chrome_options.add_argument("--disable-gpu")
    #    webdriverr_global = webdriver.Chrome(options=chrome_options)
    #    webdriverr = webdriverr_global
    #    url = 'https://catalog.onliner.by/tires' 
    #    webdriverr.get(url)
    #    soup = BeautifulSoup(webdriverr.page_source,'lxml')
    #    products = soup.find_all('div', class_='catalog-form__offers-item catalog-form__offers-item_primary')
    #    for data_got in products:
    #        #tyre_name = data_got.find('div', class_='schema-product__title')
    #        tyre_name = data_got.find('div', class_='catalog-form__description catalog-form__description_primary catalog-form__description_base-additional catalog-form__description_font-weight_semibold catalog-form__description_condensed-other')
    #        #price = data_got.find('div', class_='schema-product__price')
    #        price = data_got.find('a', class_='catalog-form__link catalog-form__link_nodecor catalog-form__link_primary-additional catalog-form__link_huge-additional catalog-form__link_font-weight_bold')
#
    ##        if tyre_name and price:
    ##            print('=-=-=-=', tyre_name.text)
    ##            print('+-=+=+=', price.text)
    #        if tyre_name and price:
    #            # проверка на лишний тект в нелегковых шинахprice
    #            check_name_is_foud = False
    #            for check_name in list_to_check:
    #                if check_name in tyre_name.text:
    #                    phrase_len = len(check_name)
    #                    wha_to_delete_start = tyre_name.text.find(check_name)
    #                    wha_to_delete_end = tyre_name.text.find(check_name) + phrase_len
    #                    text_with_no_phrase = tyre_name.text[: wha_to_delete_start] + tyre_name.text[wha_to_delete_end :]
    #                    text_with_no_phrase = text_with_no_phrase.replace('для', '')
    #                    text_to_delete1text_with_no_phrase = ''
    #                    for sh_pr in shins_phrase:
    #                            text_to_delete1text_with_no_phrase = text_with_no_phrase.replace(sh_pr, '')
    #                    tyre_name_cleaned = text_to_delete1text_with_no_phrase
    #                    tyre_name_cleaned = tyre_name_cleaned.replace('\n', '') 
    #                    tyre_name_cleaned_split = tyre_name_cleaned.split(' ')
    #                    for n in tyre_name_cleaned_split:
    #                        if n.isalnum() is True:
    #                            company_name = n
    #                            break
    #                    check_name_is_foud = True
    #                # end проверка на лишний тект в нелегковых шинах
    #            if check_name_is_foud is False:
    #                text_to_delete1 = tyre_name.text.find('шины') + 5
    #                tyre_name_cleaned = tyre_name.text[text_to_delete1 : ]
    #                tyre_name_cleaned = tyre_name_cleaned.replace('\n', '')
    #            start_str_serch = price.text.find('от') + 3
    #            end_str_search = price.text.find('р') - 1
    #            price_cleaned = price.text[start_str_serch : end_str_search]
    #            #print('5+++++', tyre_name_cleaned)
    #            #print('====', price_cleaned)
#
    #            ###### дополнительные праметры ищем: 
    #            #for data_got in products:
    #            tyre_season = data_got.find('div', class_='catalog-form__description catalog-form__description_primary catalog-form__description_small-additional catalog-form__description_bullet catalog-form__description_condensed')
    #            seas_list = ['летние', 'зимние', 'всесезонные']
    #            studded_list = ['без шипов', 'с шипами', 'возможность ошиповки']
    #            group_list_cars = ['легковых', 'внедорожников', 'минивенов', 'кроссоверов'] 
    #            group_list_lt = ['микро'] # ['микроавтобусов', 'легкогрузовых']                
    #            group_list_trucks = ['грузовых', 'строительной', 'большегрузных'] #['автобусов', 'грузовых автомобилей', 'строительной и дорожной', 'большегрузных автомобилей']
    #            group_list_agro = ['тракторов и сельскохозяйственной']
    #            tyr_group_check = False
    #            tyr_seas_check = False
    #            tyr_group = None
    #            season = None
    #            if tyre_season:
    #                split_str_prepared = tyre_season.text
    #                split_str = split_str_prepared.replace('\n', '').split(', ')
    #                season_is = []
    #                try:
    #                    if split_str[0] and split_str[0] in ['летние', 'зимние', 'всесезонные']:
    #                        season_is = split_str[0]
    #                except:
    #                    pass
    #                group_is = []
#
    #            t_gr = None
    #            split_str = data_got.find_all('div', class_='catalog-form__description catalog-form__description_primary catalog-form__description_small-additional catalog-form__description_bullet catalog-form__description_condensed')
    #            if split_str:
    #                split_str1 = split_str[1].text
    #                #print('--', split_str1) 
    #                split_str_group = split_str1    
#
    #                # для грузовых
    #                try:
    #                    if split_str_group:
    #                        group_is = split_str_group
    #                        tyr_group_check is True
    #                except:
    #                    try:
    #                        if split_str_group:
    #                            for n in group_list_cars:
    #                                if n in split_str_group:
    #                                    group_is = 'легковые'
    #                                    break
    #                            for n in group_list_lt:
    #                                if n in split_str_group:
    #                                    group_is = 'легкогруз'
    #                            #        print('---====', group_is)
    #                                    break
    #                            for n in group_list_trucks:
    #                                if n in split_str_group:
    #                                    group_is = 'грузовые'
    #                                    break
    #                            for n in group_list_agro:
    #                                if n in split_str_group:
    #                                    group_is = 'с/х'
    #                                    break
    #                        tyr_group = group_is        
    #                        tyr_group_check = True
    #                    except:
    #                        pass
    #                # END для грузовых
    #                # группа для легковых
    #                if tyr_group_check is False:
    #                    for tyr_group in group_list_cars:
    #                        if tyr_group in group_is:
    #                            t_gr = 'легковые'
    #                        #    print('tyr_group 111111', tyr_group)
    #                            break
    #                        #for tyr_group in group_list_lt:
    #                    tg_is_lt = False    
    #                    for tyr_group in group_list_lt:
    #                        if tyr_group in group_is:
    #                            t_gr = 'легкогруз'
    #                        #    print('tyr_group 111222', tyr_group, '||||', group_is)
    #                            tg_is_lt = True
    #                            break
    #                    if tg_is_lt is False:
    #                        for tyr_group in group_list_trucks:
    #                            #for tyr_group in group_list_trucks:
    #                            if tyr_group in group_is:
    #                                t_gr = 'грузовые'
    #                        #        print('tyr_group 11133', tyr_group, '||||', group_is)
    #                                break
    #                    for tyr_group in group_list_agro:
    #                        #for tyr_group in group_list_agro:
    #                        if tyr_group in group_is:
    #                            t_gr = 'с/х'
    #                    #        print('tyr_group 111', tyr_group)
    #                            break
    #                    tyr_group = t_gr
    #                # END группа для легковых    
    #                # сезонность
    #                studded_is = []                       # ШИПЫ - тут доработать
    #                for s_el in seas_list:
    #                    if s_el in tyre_season.text:
    #                        season = s_el
    #                    #    if 'BEL-318' in tyre_name_cleaned:
    #                    #        print('group_is ========88888=', tyre_season.text)  
    #                    #        print('group_is =====================', season)  
    #                # END сезонность
    #                # шипы
    #                for studded_el in studded_list:
    #                    if studded_el in tyre_season.text:
    #                        studded = studded_el
    #                #print( season, '          ', studded)
    #                t_gr = None
    #                # END 
    #    # выдираем типоразмер для добавления в словарь
    #            tyresize = str
    #            for n in reg_list:
    #                result = re.search(rf'(?i){n}', tyre_name_cleaned)
    #                if result:
    #                    tyresize = result.group(0)
    #                    #print(tyresize)
    #                    ### удаление среза с типоразмером и всем что написано перед типоразмером
    #                    left_before_size_data_index = tyre_name_cleaned.index(result.group(0))
    #                    if left_before_size_data_index > 0:
    #                        str_left_data = tyre_name_cleaned[0:left_before_size_data_index-1]
    #                        tyresize_length = len(result.group(0)) + 1 
    #                        right_after_size_data_index = tyre_name_cleaned.index(result.group(0)) + tyresize_length
    #                        str_right_data = tyre_name_cleaned[right_after_size_data_index : ]
    #                    product_name = str_left_data
    #                    if check_name_is_foud is False:
    #                        company_name = product_name.split(' ')[0]
    #                    tyre_param = str_right_data
    #            values = price_cleaned, tyresize, product_name, tyre_param, company_name, season, tyr_group, #studded 
    #            print('||', price_cleaned, tyresize, product_name, tyre_param, company_name, season, tyr_group)  # 805,00 275/70R22.5    Белшина Escortera BEL-318  Белшина летние грузовые
    #            goods_dict[tyre_name_cleaned] = values                                                                      # ПОДПРАВИТЬ КЛЮЧИ _ НЕ ВСЕ ПОПАДУТ ВЕДБ
    #    #for k, v in goods_dict.items():
    #    #    print('K==', k, 'V==', v, 'KV')
    #    onliner_companies_list = []  # список компаний-производителей Oliner
    #    for v in goods_dict.values():
    #        if v[4] and v[4].isdigit() is False:
    #            onliner_companies_list.append(v[4])
    #    onliner_companies_list = list(set(onliner_companies_list))  
    #    temp_goods_dict_list_k_names_to_delete = []
    #    for v in goods_dict.values():
    #        if v[4] and v[4] in onliner_companies_list:                 # СЕЙЧАС ВЫДАЕТ ВСЕХ ПРОИЗВОДИТЕЛЕЙ  ВСЕЮ ПРОДУКЦИЮ или подкинутых пользователем
    #            pass
    #        else:
    #            temp_goods_dict_list_k_names_to_delete.extend(v[4])
    #    for k_name in temp_goods_dict_list_k_names_to_delete:
    #        goods_dict.pop(k_name)
    #    # сопоставление с БД  и запись в БД конкурентов (Onliner):
    #    onliner_compet_obj_tyre_bulk_list = []
    #    list_tyre_sizes = []
    #    from tyres import models as tyres_models
    #    from dictionaries import models as dictionaries_models
    #    tyres_in_bd = tyres_models.Tyre.objects.all()
    #    for tyre in tyres_in_bd:
    #        for k, v in goods_dict.items():
    #            #   print(k, len(k), 'v', v)
    #            if tyre.tyre_size.tyre_size == v[1]:                                                                                            #  ПРОСМОТР ВСЕХ СПАРСЕННЫХ 
    #                # Goodyear EfficientGrip Performance 2 205/60R16 92H 50 v ('\n341,08', '205/60R16', 'Goodyear EfficientGrip Performance 2', '92H', 'Goodyear', 'летние', 'легковые')                                                                                   #  ПРОСМОТР ВСЕХ СПАРСЕННЫХ 
    #                coma = v[0].find(',')
    #                pr = float
    #                name_competitor, created = dictionaries_models.CompetitorModel.objects.get_or_create(
    #                    competitor_name = v[4] 
    #                )
    #              ##     print('HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH', v[6])
    #                season_usage = dictionaries_models.SeasonUsageModel.objects.filter(season_usage_name=v[5]) 
    #                if season_usage:
    #                    season_usage = season_usage[0]
    #                else:
    #                    season_usage = None 
    #                if coma:
    #                    no_with_coma = v[0].replace(',', '.').replace('\n', '')
    #                    try:
    #                        pr = float(no_with_coma) 
    #                    except:
    #                        pr = None
    #                tyre_group_ussage = dictionaries_models.TyreGroupModel.objects.filter(tyre_group=v[6])
    #                if tyre_group_ussage:
    #                    tyre_group_ussage = tyre_group_ussage[0]
    #                else:
    #                    tyre_group_ussage = None 
    #                if coma:
    #                    no_with_coma = v[0].replace(',', '.').replace('\n', '')
    #                    try:
    #                        pr = float(no_with_coma) 
    #                    except:
    #                        pr = None
    #                list_tyre_sizes.append(v[1])
    #                print('onliner.by hihhihi', 'pr=', pr, 'name_competitor', name_competitor, 'v[1]', v[1], 'v[2]', v[2], 'v[3]', v[3], 'season_usage', season_usage, tyre_group_ussage)
#
    #                from prices import models
    #                onliner_compet_obj_tyre_bulk_list.append(models.CompetitorSiteModel(
    #                    site = 'onliner.by',
    #                    #tyre = tyre,
    #                    currency = dictionaries_models.Currency.objects.get(currency='BYN'),
    #                    price = pr,
    #                    date_period = datetime.datetime.today(),
    #                    #developer = v[4],
    #                    developer = name_competitor,
    #                    tyresize_competitor = v[1],
    #                    name_competitor = v[2], 
    #                    parametres_competitor = v[3],
    #                    season = season_usage,
    #                    group = tyre_group_ussage,
    #                )        
    #                )
    #    import itertools            
    #    bulk_onl_compet = models.CompetitorSiteModel.objects.bulk_create(onliner_compet_obj_tyre_bulk_list)
    #    list_tyre_sizes = set(list_tyre_sizes)
    #    for t_szz in list_tyre_sizes:
    #        for obbj, comparative_analys_tyres_model_object in itertools.product(models.CompetitorSiteModel.objects.filter(tyresize_competitor=t_szz, site = 'onliner.by'), models.ComparativeAnalysisTyresModel.objects.filter(tyre__tyre_size__tyre_size=t_szz)):
    #                obbj.tyre_to_compare.add(comparative_analys_tyres_model_object) 
#
    #    return 'fghfgh'
    
#    sdfsdfsdsdf()
    run_the_parscin_script()
    


if __name__ == "__main__":
    main()

