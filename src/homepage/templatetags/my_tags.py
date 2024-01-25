from django import template
register = template.Library()
import requests
import datetime
from prices import models as prices_models

USD_ENDPOINT = 'https://www.nbrb.by/api/exrates/rates/431'
ALL_CURRENCIES_ENDPOINT = 'https://www.nbrb.by/api/exrates/rates?periodicity=0'

@register.simple_tag
def currency_rate_usd():  # {% currency_rate obj pbj2  %}
    #res = requests.get(USD_ENDPOINT)
    #return res.json().get('Cur_OfficialRate')
    res2 = requests.get(ALL_CURRENCIES_ENDPOINT)  
    usd_value = None
    for nn in res2.json():
        #print(nn)
        if nn.get('Cur_ID') == 431 and nn.get('Cur_Name') == 'Доллар США':
            #print('Доллар США =', nn.get('Cur_OfficialRate'))
            usd_value = nn.get('Cur_OfficialRate')
    return usd_value

@register.simple_tag
def currency_rate_russia_rub():  # {% currency_rate obj pbj2  %}
    res2 = requests.get(ALL_CURRENCIES_ENDPOINT)  
    russia_rub_value = None
    for nn in res2.json():
        #print(nn)
        if nn.get('Cur_ID') == 456 and nn.get('Cur_Name') == 'Российских рублей':
            #print('Российских рублей =', nn.get('Cur_OfficialRate'))
            russia_rub_value = nn.get('Cur_OfficialRate')
    return russia_rub_value

@register.simple_tag
def current_date():
    #print('datetime.date.now()', datetime.datetime.now().date())
    return datetime.datetime.now().date().strftime("%d.%m.%Y")  

@register.simple_tag
def currency_on_date():  
    ## по курсу НАЦБАНКА РБ
    #usd_got_from_nbrb = 'https://www.nbrb.by/api/exrates/rates/431'        # долл. США на сегодня если ничего больше не введено пользователем
    #rub_russ_got_from_nbrb = 'https://www.nbrb.by/api/exrates/rates/456'        # росс. рубль на сегодня если ничего больше не введено пользователем
    #CURRENCY_TO_LOOKUP = usd_got_from_nbrb
    ##if prices_models.COMPETITORS_DATE_FROM_USER_ON_FILTER:
    #if prices_models.CURRENCY_DATE_GOT_FROM_USER:
    #    usd_got_from_nbrb = 431
    #    rub_russ_got_from_nbrb = 456
    #    currency_too_look_for_id = usd_got_from_nbrb
    #    CURRENCY_TO_LOOKUP = f'https://www.nbrb.by/api/exrates/rates/{currency_too_look_for_id}?ondate={prices_models.CURRENCY_DATE_GOT_FROM_USER}'  
    #res = requests.get(CURRENCY_TO_LOOKUP)  
    #curr_value = None
    #currency = None
    #shown_date = None
    ##currency_and_its_val = None
    ##print('RES', res.json())    # RES {'Cur_ID': 431, 'Date': '2023-10-09T00:00:00', 'Cur_Abbreviation': 'USD', 'Cur_Scale': 1, 'Cur_Name': 'Доллар США', 'Cur_OfficialRate': 3.3605}
    #try:
    #    if res.json().get('Cur_ID') == 456 and res.json().get('Cur_Name') == 'Российских рублей':
    #        curr_value = res.json().get('Cur_OfficialRate')
    #        #print('curr_value', curr_value)
    #        currency = '100 RUB'
    #        shown_date = res.json().get('Date').replace('T00:00:00', '')
    #    if res.json().get('Cur_ID') == 431 and res.json().get('Cur_Name') == 'Доллар США':
    #        curr_value = res.json().get('Cur_OfficialRate')
    #        #print('curr_value', curr_value)
    #        currency = '1 USD'
    #        shown_date = res.json().get('Date').replace('T00:00:00', '')   
#
    #    if shown_date and curr_value and currency:
    #        print('currency, curr_value, shown_date ++++++++', currency, curr_value, shown_date)
    #        return currency, curr_value, shown_date
    #        
    #    return None
    #except:
    #    return 'Нет данных', 0, 'Ошибка сервера НБ РБ'
    ## END по курсу НАЦБАНКА РБ

    # КУРС ПО ЦБ РФ:
    cur_date = current_date()  
    dtm_obj = datetime.datetime.strptime(cur_date, f'%d.%m.%Y')
    cur_date_string = dtm_obj.strftime('%d/%m/%Y')
    if prices_models.CURRENCY_DATE_GOT_FROM_USER:
        dtm_obj = datetime.datetime.strptime(prices_models.CURRENCY_DATE_GOT_FROM_USER, f'%Y-%m-%d')
        cur_date_string = dtm_obj.strftime('%d/%m/%Y')    
    parsing_adress = f'http://www.cbr.ru/scripts/XML_daily.asp?date_req={cur_date_string}' #&VAL_NM_RQ=R01235'

    res = requests.get(parsing_adress)  
    curr_value = None
    currency = None
    shown_date = None  

    res_text = res.text
    start_point = res_text.find('R01235"')
    text_with_no_beginn = res_text[start_point:]
    end_point = text_with_no_beginn.find('/VunitRate')
    res_cut = text_with_no_beginn[:end_point]

    start_point_val = res_cut.find('<Value>') + 7
    text_with_no_beginn_val = res_cut[start_point_val:] 
    end_point_val = text_with_no_beginn_val.find('</Value>')   
    res_cut_val = text_with_no_beginn_val[:end_point_val].replace(',', '.')
    #print('res_cut_val ==', res_cut_val) 
    curr_value = float(res_cut_val)
    if curr_value:
        currency = '1 USD'
        shown_date = prices_models.CURRENCY_DATE_GOT_FROM_USER
        return currency, curr_value, shown_date
    return 'Нет данных', 0, 'Ошибка сервера НБ РБ'
    # END КУРС ПО ЦБ РФ:



############### ЗАТЫЧКА  - УБРАТЬ:
#@register.simple_tag
#def currency_on_date():
#    return 'BBBBB', 10, '2012-05-05'
######################################