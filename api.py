import requests

from conf import API_KEY

API_URL_BASE = 'https://api.themoviedb.org/3'


def get_popular(page=None):
    api_url = f'{API_URL_BASE}/movie/popular?api_key={API_KEY}&page={page}'
    return requests.get(api_url).json()


def get_top_rated(page=None):
    api_url = f'{API_URL_BASE}/movie/top_rated?api_key={API_KEY}&page={page}'
    return requests.get(api_url).json()


def get_movie_detail(movie_id):
    api_url = f'{API_URL_BASE}/movie/{movie_id}?api_key={API_KEY}'
    return requests.get(api_url).json()


def get_movie_cast(movie_id):
    api_url = f'{API_URL_BASE}/movie/{movie_id}/credits?api_key={API_KEY}'
    return requests.get(api_url).json().get('cast')


def get_person_detail(person_id):
    api_url = f'{API_URL_BASE}/person/{person_id}?api_key={API_KEY}'
    return requests.get(api_url).json()
