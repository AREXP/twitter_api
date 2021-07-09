import argparse
import math
import os
import requests

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
TOKEN = os.environ.get('BEARER_TOKEN')

API_URL = 'https://api.themoviedb.org/3'


def connect_to_endpoint(url, params={}):
    headers = {
        'Authorization': f'Bearer {TOKEN}',
        'Content-Type': 'application/json;charset=utf-8',
    }
    response = requests.request('GET', url, headers=headers,
                                params=params)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def get_popular_movies(page=1):
    url = f'{API_URL}/discover/movie'
    params = {
        'sort_by': 'popularity.desc',
        'page': page,
    }
    response = connect_to_endpoint(url, params)
    return response.get('results')


def get_country(movie_id):
    url = f'{API_URL}/movie/{movie_id}'
    response = connect_to_endpoint(url)
    countries = response['production_countries']
    return 'Not specified' if not countries else countries[0]['name']


def get_top_movies(number):
    total_pages = math.ceil(number / 20)
    top_movies = []
    for page in range(1, total_pages + 1):
        top_movies += get_popular_movies(page)
    if top_movies is None or len(top_movies) < number:
        return 'Some error occurred while requesting movies'
    result = [(f'{movie["id"]}/{movie["title"]}/{position + 1}/'
               f'{movie["release_date"]}/{movie["popularity"]}/'
               f'{get_country(movie["id"])}')
              for position, movie in enumerate(top_movies[:number])]
    return result


def get_country(movie_id):
    url = f'{API_URL}/movie/{movie_id}'
    response = connect_to_endpoint(url)
    countries = response['production_countries']
    return 'Not specified' if not countries else countries[0]['name']


def get_person_info(person_id):
    url = f'{API_URL}/person/{person_id}'
    response = connect_to_endpoint(url)
    return f'{response["place_of_birth"]}/{response["birthday"]}'


def get_movie_actors(movie_id):
    url = f'{API_URL}/movie/{movie_id}/credits'
    response = connect_to_endpoint(url)
    actors = [person for person in response['cast']
              if person['known_for_department'] == 'Acting']
    return actors


def get_5_actors(movie_id):
    actors = get_movie_actors(movie_id)
    if len(actors) < 5:
        return 'Some error occurred while requesting credits'
    result = [(f'{actor["name"]}/{actor["character"]}/'
               f'{get_person_info(actor["id"])}')
              for actor in actors[:5]]
    return result


if __name__ == '__main__':
    description = 'App to obtain movies and actors info from themoviedb.org'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-n', '--number',
                        help=('Specify the required number of films for '
                              'output'),
                        type=int)
    parser.add_argument('-i', '--id',
                        help=('Specify the id of the movie for '
                              'the output of it\'s 5 actors'),
                        type=int)
    args = parser.parse_args()
    if args.number:
        result = get_top_movies(args.number)
        print(*result, sep='\n', end='\n')
    if args.id:
        result = get_5_actors(args.id)
        print(*result, sep='\n', end='\n')
