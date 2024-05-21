import os
from dotenv import dotenv_values

# path in root
# env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'priv.env')
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')

#load
config = dotenv_values(env_path)

#fetch
REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT')
APCA_API_KEY_ID = os.getenv('APCA_API_KEY_ID')
APCA_API_SECRET_KEY = os.getenv('APCA_API_SECRET_KEY')
APCA_BASE_URL = os.getenv('APCA_BASE_URL')
