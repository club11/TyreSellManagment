



def main():
    import datetime
    from prices import views

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
            print(' +++++++++++ === =====++++++++the programm is FULLFILLED')
            views.running_programm()

            
            from selenium.webdriver.chrome.service import Service as ChromeService
            from webdriver_manager.chrome import ChromeDriverManager


            
            
            from selenium import webdriver
            import time
            from bs4 import BeautifulSoup
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
            options = Options()
            options.add_argument("disable-infobars")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--no-sandbox")
            options.add_argument('--headless=new')
            #webdriverr_global = webdriver.Chrome(options=options)
                                                   
            webdriverr_global = webdriver.Chrome(options=options,service=ChromeService(ChromeDriverManager().install()))

            url = 'https://catalog.onliner.by/tires'
            webdriverr = webdriverr_global
            webdriverr.get(url)
            time.sleep(2)
            webdriverr.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)
            soup = BeautifulSoup(webdriverr.page_source,'lxml')
            try:

                #pages = soup.find('ul', class_='catalog-pagination__pages-list')
                #urls = []
                #if pages:
                #    links = pages.find_all('a', class_='catalog-pagination__pages-link')
                #    for link in links:
                #        pageNum = int(link.text) #if link.text.isdigit() else None
                #        print('pageNum', pageNum)
                #        if pageNum != None:
                #            urls.append(pageNum)
                #    #print('links', links)
                #    print('urls', urls)
                pag = soup.find('div', class_='catalog-form__header-part catalog-form__header-part_1')
                print('=======', pag.text)

                webdriverr.error_handle
                webdriverr.quit()
            except:
                print('+++ERROR+++')
                webdriverr.quit()

        print('PROFECY IS FULLFILLED !!!!! OMENS IN THE SKY')

        return 'the programm is fullfilled'



    run_the_parscin_script()


if __name__ == "__main__":
    main()


#import os
#os.environ["DJANGO_SETTINGS_MODULE"] = "proj.settings"
#import django
#django.setup()
#
#def give_me():
#    from django.apps import apps
#    for app in apps.get_app_configs():
#        print(app, app.name, app.label)
#
#give_me()