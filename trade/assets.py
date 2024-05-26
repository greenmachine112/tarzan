import sys
import os

from dotenv import load_dotenv
#load_dotenv(dotenv_path='priv.env')
load_dotenv()

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from clients.alpaca_client import makeRequest

APCA_BASE_URL = os.getenv("APCA_BASE_URL")

#By symbol/ticker only. For crypto, coin symbol must be succeeded by fiat currency symbol. Eg) Bitcoin = BTCUSD
def getAsset(assetId_or_Symbol):
    endpoint = f"{APCA_BASE_URL}/assets/{assetId_or_Symbol}"  #Endpoint
    return makeRequest('GET', endpoint)