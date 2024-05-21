import sys
import os

from dotenv import load_dotenv
#load_dotenv(dotenv_path='priv.env')
load_dotenv()

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from clients.alpaca_client import makeRequest

APCA_BASE_URL = os.getenv("APCA_BASE_URL")

#By symbol/ticker only. For crypto, coin symbol must be succeeded by fiat currency symbol. Eg) Bitcoin = BTCUSD
def getAsset(asset_id_or_symbol):
    endpoint = f"{APCA_BASE_URL}/assets/{asset_id_or_symbol}"  #Endpoint
    return makeRequest('GET', endpoint)