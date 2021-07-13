from os import environ

from dotenv import load_dotenv

load_dotenv()

API_KEY = environ.get('API_KEY')
