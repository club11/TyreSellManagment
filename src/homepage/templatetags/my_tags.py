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
    usd_got_from_nbrb = 'https://www.nbrb.by/api/exrates/rates/431'        # долл. США на сегодня если ничего больше не введено пользователем
    rub_russ_got_from_nbrb = 'https://www.nbrb.by/api/exrates/rates/456'        # росс. рубль на сегодня если ничего больше не введено пользователем
    CURRENCY_TO_LOOKUP = usd_got_from_nbrb
    #if prices_models.COMPETITORS_DATE_FROM_USER_ON_FILTER:
    if prices_models.CURRENCY_DATE_GOT_FROM_USER:
        usd_got_from_nbrb = 431
        rub_russ_got_from_nbrb = 456
        currency_too_look_for_id = usd_got_from_nbrb
    
        #print('models.COMPETITORS_DATE_FROM_USER_ON_FILTER', models.COMPETITORS_DATE_FROM_USER_ON_FILTER[0])
        #CURRENCY_TO_LOOKUP = f'https://www.nbrb.by/api/exrates/rates/456?ondate={prices_models.COMPETITORS_DATE_FROM_USER_ON_FILTER[0]}'    # https://www.nbrb.by/api/exrates/rates/456?ondate=2022-1-1  # models.COMPETITORS_DATE_FROM_USER_ON_FILTER: ['2023-03-12']
        #CURRENCY_TO_LOOKUP = f'https://www.nbrb.by/api/exrates/rates/456?ondate={prices_models.CURRENCY_DATE_GOT_FROM_USER}'   
        CURRENCY_TO_LOOKUP = f'https://www.nbrb.by/api/exrates/rates/{currency_too_look_for_id}?ondate={prices_models.CURRENCY_DATE_GOT_FROM_USER}'

        pass                           
    res = requests.get(CURRENCY_TO_LOOKUP)  
    curr_value = None
    currency= None
    shown_date = None
    #currency_and_its_val = None
    #print('RES', res.json())    # RES {'Cur_ID': 431, 'Date': '2023-10-09T00:00:00', 'Cur_Abbreviation': 'USD', 'Cur_Scale': 1, 'Cur_Name': 'Доллар США', 'Cur_OfficialRate': 3.3605}
    try:
        if res.json().get('Cur_ID') == 456 and res.json().get('Cur_Name') == 'Российских рублей':
            curr_value = res.json().get('Cur_OfficialRate')
            #print('curr_value', curr_value)
            currency = '100 RUB'
            shown_date = res.json().get('Date').replace('T00:00:00', '')

        if res.json().get('Cur_ID') == 431 and res.json().get('Cur_Name') == 'Доллар США':
            curr_value = res.json().get('Cur_OfficialRate')
            #print('curr_value', curr_value)
            currency = '1 USD'
            shown_date = res.json().get('Date').replace('T00:00:00', '')   

#       if nn.get('Cur_ID') == 431 and nn.get('Cur_Name') == 'Доллар США':
#           curr_value = nn.get('Cur_OfficialRate')
#           currency = nn.get('Cur_Name')
#           currency_and_its_val = currency, curr_value
        if shown_date and curr_value and currency:
            print('currency, curr_value, shown_date ++++++++', currency, curr_value, shown_date)
            return currency, curr_value, shown_date
        return None
    except:
        return 'Нет данных', 0, 'Ошибка сервера НБ РБ'


############### ЗАТЫЧКА  - УБРАТЬ:
@register.simple_tag
def currency_on_date():
    return 'BBBBB', 10, '2012-05-05'
######################################