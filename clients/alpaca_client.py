import requests
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.config import APCA_API_KEY_ID, APCA_API_SECRET_KEY
from src.styles import GREEN, RESET

def makeRequest(method, endpoint, headers=None, params=None, data=None):
    url = endpoint    
    default_headers = {
        'APCA-API-KEY-ID': APCA_API_KEY_ID,
        'APCA-API-SECRET-KEY': APCA_API_SECRET_KEY,
        'accept': 'application/json',
    }
    print(f"{GREEN}Alpaca client created successfully{RESET}")

    if headers:
        default_headers.update(headers)
    
    response = requests.request(method, url, headers=default_headers, params=params, json=data)
    response.raise_for_status()  #Raise an exception for HTTP errors
    return response.json()