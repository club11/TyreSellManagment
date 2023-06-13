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
    return datetime.datetime.now().date().strftime("%Y-%B-%d")  

@register.simple_tag
def currency_on_date():  
    CURRENCY_TO_LOOKUP = 'https://www.nbrb.by/api/exrates/rates/456'        # росс. рубль на сегодня если ничего больше не введено пользователем
    #if prices_models.COMPETITORS_DATE_FROM_USER_ON_FILTER:
    if prices_models.CURRENCY_DATE_GOT_FROM_USER:
    
        #print('models.COMPETITORS_DATE_FROM_USER_ON_FILTER', models.COMPETITORS_DATE_FROM_USER_ON_FILTER[0])
        #CURRENCY_TO_LOOKUP = f'https://www.nbrb.by/api/exrates/rates/456?ondate={prices_models.COMPETITORS_DATE_FROM_USER_ON_FILTER[0]}'    # https://www.nbrb.by/api/exrates/rates/456?ondate=2022-1-1  # models.COMPETITORS_DATE_FROM_USER_ON_FILTER: ['2023-03-12']
        CURRENCY_TO_LOOKUP = f'https://www.nbrb.by/api/exrates/rates/456?ondate={prices_models.CURRENCY_DATE_GOT_FROM_USER}'
        pass                           
    res = requests.get(CURRENCY_TO_LOOKUP)  
    curr_value = None
    currency= None
    shown_date = None
    #currency_and_its_val = None
    if res.json().get('Cur_ID') == 456 and res.json().get('Cur_Name') == 'Российских рублей':
        #print('Российских рублей =', nn.get('Cur_OfficialRate'))
        curr_value = res.json().get('Cur_OfficialRate')
        currency = 'рубль РФ'
        shown_date = res.json().get('Date').replace('T00:00:00', '')
#   if nn.get('Cur_ID') == 431 and nn.get('Cur_Name') == 'Доллар США':
#       curr_value = nn.get('Cur_OfficialRate')
#       currency = nn.get('Cur_Name')
#       currency_and_its_val = currency, curr_value
    if shown_date and curr_value and currency:
        #print('currency, curr_value, shown_date ++++++++', currency, curr_value, shown_date)
        return currency, curr_value, shown_date
    return None


############# ЗАТЫЧКА  - УБРАТЬ:
@register.simple_tag
def currency_on_date():
    return 'BBBBB', 10, '2012-05-05'
####################################