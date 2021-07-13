import sys

import requests

from conf import API_KEY

API_URL_BASE = 'https://api.themoviedb.org/3'
API_URL_HEADERS = {'Content-Type': 'application/json'}
PAGE_SIZE = 20
NUMBER_OF_ACTORS = 5


def get_popular(page=None):
    api_url = f'{API_URL_BASE}/movie/popular?api_key={API_KEY}&page={page}'
    return requests.get(api_url).json()


def get_rate(page=None):
    api_url = f'{API_URL_BASE}/movie/top_rated?api_key={API_KEY}&page={page}'
    return requests.get(api_url).json()


def get_movie_detail(movie_id):
    api_url = f'{API_URL_BASE}/movie/{movie_id}?api_key={API_KEY}'
    return requests.get(api_url).json()


def get_movie_cast(movie_id):
    api_url = f'{API_URL_BASE}/movie/{movie_id}/credits?api_key={API_KEY}'
    response = requests.get(api_url).json()
    return response.get('cast')


def get_person_detail(person_id):
    api_url = f'{API_URL_BASE}/person/{person_id}?api_key={API_KEY}'
    return requests.get(api_url).json()


def search_film_position_in_page(movie_id, movies):
    for position, movie in enumerate(movies):
        if movie['id'] == movie_id:
            return position+1


def get_place_in_rate(movie_id):
    total_pages = get_rate().get('total_pages')
    for page_number in range(1, total_pages+1):
        movies = get_rate(page_number).get('results')
        position_on_page = search_film_position_in_page(movie_id, movies)
        if position_on_page and page_number == 1:
            return position_on_page
        elif position_on_page and page_number > 1:
            return page_number*PAGE_SIZE+position_on_page


def get_movie_info(movie):
    id = movie.get('id')
    title = movie.get('title')
    release_date = movie.get('release_date')
    rating = movie.get('vote_average')
    movie_details = get_movie_detail(id)
    place_in_rate = get_place_in_rate(id)
    production_country = movie_details.get(
        'production_countries')[0].get('iso_3166_1')
    print(f'{id} / {title} / {place_in_rate} / {release_date} / '
          f'{rating} / {production_country}')
    movie_cast = get_movie_cast(id)
    actors = []
    for cast in movie_cast:
        if cast['known_for_department'] == 'Acting':
            actors.append(cast)
    for actor in actors[:NUMBER_OF_ACTORS]:
        id = actor.get('id')
        name = actor.get('name')
        character = actor.get('character')
        actor_info = get_person_detail(id)
        birthday = actor_info.get('birthday')
        place_of_birth = actor_info.get('place_of_birth')
        print(f"{name} / {character} / {birthday} / {place_of_birth}")


def main(n):
    movies_counter = 0
    total_pages = get_popular().get('total_pages')
    for page_number in range(1, total_pages+1):
        popular_movies = get_popular(page_number).get('results')
        for movie in popular_movies:
            if movies_counter < n:
                print(f'----------{movies_counter+1}----------')
                get_movie_info(movie)
                movies_counter += 1
            else:
                exit()


if __name__ == '__main__':
    n = int(sys.argv[1])
    main(n)
