
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
    #        if tyre_name and price:
    #            print('=-=-=-=', tyre_name.text)
    #            print('+-=+=+=', price.text)


        return 'fghfgh'
    
#    sdfsdfsdsdf()
    run_the_parscin_script()
    


if __name__ == "__main__":
    main()

