import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from clients.alpaca_client import makeRequest

from dotenv import load_dotenv
#load_dotenv(dotenv_path='priv.env')
load_dotenv()

APCA_BASE_URL = os.getenv("APCA_BASE_URL")