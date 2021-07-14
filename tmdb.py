import argparse
import math
import os
import requests
import sys

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
TOKEN = os.environ.get('BEARER_TOKEN')
API_URL = 'https://api.themoviedb.org/3'
MOVIES_SORT_KEY = 'popularity.desc'
MOVIES_PER_PAGE = 20
MOVIES_HEADER = ('ID / TITLE / POSITION / RELEASE DATE / RATING / '
                 'COUNTRIES OF ORIGIN')
ACTORS_DEPARTMENT = 'Acting'
ACTORS_TOP = 5
ACTORS_HEADER = 'NAME / CHARACTER / PLACE OF BIRTH / BIRTHDAY'


class InvalidParameterError(Exception):
    pass


class ValidateParameter(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if values <= 0:
            sys.exit('This parameter must be positive integer number')
        setattr(namespace, self.dest, values)


def request_data(endpoint, params=None):
    url = API_URL + endpoint
    headers = {
        'Authorization': f'Bearer {TOKEN}',
        'Content-Type': 'application/json;charset=utf-8',
    }
    response = requests.request('GET',
                                url,
                                headers=headers,
                                params=params)
    response.raise_for_status()
    return response.json()


def get_popular_movies(page):
    endpoint = '/discover/movie'
    params = {
        'sort_by': MOVIES_SORT_KEY,
        'page': page,
    }
    response = request_data(endpoint, params)
    return response.get('results', [])


def get_countries(movie_id):
    endpoint = f'/movie/{movie_id}'
    response = request_data(endpoint)
    countries = [country.get('name')
                 for country in response.get('production_countries', [])]
    result = ', '.join(countries)
    return result or 'Not specified'


def get_top_movies(number):
    total_pages = math.ceil(number / MOVIES_PER_PAGE)
    top_movies = []
    for page in range(1, total_pages + 1):
        top_movies += get_popular_movies(page)

    result = []
    for position, movie in enumerate(top_movies[:number], start=1):
        id = movie.get('id')
        title = movie.get('title')
        date = movie.get('release_date')
        rating = movie.get('popularity')
        origin = get_countries(id)
        info = f'{id} / {title} / {position} / {date} / {rating} / {origin}'
        result.append(info)
    return result


def get_person_info(person_id):
    endpoint = f'/person/{person_id}'
    response = request_data(endpoint)
    return f'{response["place_of_birth"]} / {response["birthday"]}'


def get_movie_actors(movie_id):
    endpoint = f'/movie/{movie_id}/credits'
    response = request_data(endpoint)
    actors = [person for person in response['cast']
              if person['known_for_department'] == ACTORS_DEPARTMENT]
    return actors


def get_top_actors(movie_id):
    actors = get_movie_actors(movie_id)
    result = []
    for actor in actors[:ACTORS_TOP]:
        name = actor.get('name')
        character = actor.get('character')
        birth_info = get_person_info(actor.get('id'))
        info = f'{name} / {character} / {birth_info}'
        result.append(info)
    return result


if __name__ == '__main__':
    description = 'App to obtain movies and actors info from themoviedb.org'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-n',
                        '--number',
                        action=ValidateParameter,
                        help=('Specify the required number of films for '
                              'output'),
                        type=int)
    parser.add_argument('-i',
                        '--id',
                        help=('Specify the id of the movie for '
                              'the output of it\'s 5 actors'),
                        type=int)
    args = parser.parse_args()

    try:
        if args.number:
            header = MOVIES_HEADER
            result = get_top_movies(args.number)
        elif args.id:
            header = ACTORS_HEADER
            result = get_top_actors(args.id)
        else:
            raise InvalidParameterError
        print(header, *result, sep='\n')
    except requests.exceptions.HTTPError as err:
        print(err)
    except InvalidParameterError:
        print('Invalid parameter. Use -h to get help')
