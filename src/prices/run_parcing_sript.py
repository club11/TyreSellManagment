import requests


bel_market_parcing_request = 'http://127.0.0.1:8000/prices/'
russia_market_parcing_request = 'http://127.0.0.1:8000/prices/prices_russia'



def run_parcing_script_all_markets_bel_and_russia():
    requests.get(bel_market_parcing_request)  
    requests.get(russia_market_parcing_request)  

    return 'request is done'