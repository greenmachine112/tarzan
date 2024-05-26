import os
from dotenv import dotenv_values

#path in root
#envPath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'priv.env')
envPath = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')

#load
config = dotenv_values(envPath)

#manual set up you mf
os.environ.update(config)

#fetch
REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT')
APCA_API_KEY_ID = os.getenv('APCA_API_KEY_ID')
APCA_API_SECRET_KEY = os.getenv('APCA_API_SECRET_KEY')
APCA_BASE_URL = os.getenv('APCA_BASE_URL')
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
ALPHA_VANTAGE_API_KEY=os.getenv('ALPHA_VANTAGE_API_KEY')