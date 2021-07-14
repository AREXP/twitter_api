import argparse

from api import (get_movie_cast, get_movie_detail, get_person_detail,
                 get_popular, get_top_rated)

PAGE_SIZE = 20
NUMBER_OF_ACTORS = 5
NO_INFO = 'No info'


def search_film_position_in_page(movie_id, movies):
    for position, movie in enumerate(movies, start=1):
        if movie['id'] == movie_id:
            return position


def get_place_in_rate(movie_id):
    try:
        response = get_top_rated()
    except Exception as e:
        print(f'Ошибка при выполнении запроса '
              f'GET /movie/top_rated: {e}')
    total_pages = response.get('total_pages')
    results = response.get('results')
    position_on_page = search_film_position_in_page(movie_id, results)
    if position_on_page and total_pages == 1:
        return position_on_page
    for page_number in range(2, total_pages + 1):
        try:
            movies = get_top_rated(page_number).get('results')
        except Exception as e:
            print(f'Ошибка при выполнении запроса '
                  f'GET /movie/top_rated: {e}')
        position_on_page = search_film_position_in_page(movie_id, movies)
        if position_on_page:
            return page_number * PAGE_SIZE + position_on_page


def get_production_countries(movie_id):
    try:
        production_countries = get_movie_detail(movie_id).get(
            'production_countries')
    except Exception as e:
        print(f'Ошибка при выполнении запроса '
              f'GET /movie/{movie_id}: {e}')
    return ', '.join([pc.get('iso_3166_1') for pc in production_countries])


def movie_info(results, movies_counter, n):
    for movie in results:
        if movies_counter < n:
            movie_id = movie.get('id')
            title = movie.get('title')
            if title is None:
                title = NO_INFO
            release_date = movie.get('release_date')
            if release_date is None:
                release_date = NO_INFO
            rating = movie.get('vote_average')
            if rating is None:
                rating = NO_INFO
            place_in_rate = get_place_in_rate(movie_id)
            if place_in_rate is None:
                place_in_rate = NO_INFO
            production_countries = get_production_countries(movie_id)
            if production_countries is None:
                production_countries = NO_INFO
            print('-' * 140)
            print(f'{movie_id:<10} {title:<70} {place_in_rate:<15} '
                  f'{release_date:<15} {rating:<15} '
                  f'{production_countries:<50}')
            movies_counter += 1
        else:
            exit()
    return movies_counter


def show_actors(movie_id):
    headers = ('NAME', 'CHARACTER', 'BIRTHDAY', 'PLACE_OF_BIRTH')
    print('%-40s %-40s %-15s %-50s' % headers)
    try:
        movie_cast = get_movie_cast(movie_id)
    except Exception as e:
        print(f'Ошибка при выполнении запроса '
              f'GET /movie/{movie_id}/credits: {e}')
    actors = []
    for cast in movie_cast:
        if cast['known_for_department'] == 'Acting':
            actors.append(cast)
    for actor in actors[:NUMBER_OF_ACTORS]:
        actor_id = actor.get('id')
        name = actor.get('name')
        if name is None:
            name = NO_INFO
        character = actor.get('character')
        if character is None:
            character = NO_INFO
        try:
            actor_info = get_person_detail(actor_id)
        except Exception as e:
            print(f'Ошибка при выполнении запроса '
                  f'GET /person/{actor_id}: {e}')
        birthday = actor_info.get('birthday')
        if birthday is None:
            birthday = NO_INFO
        place_of_birth = actor_info.get('place_of_birth')
        if place_of_birth is None:
            place_of_birth = NO_INFO
        print('-' * 140)
        print(
            f'{name:<40} {character:<40} {birthday:<15} {place_of_birth:<50}'
        )


def show_movies(n):
    movies_counter = 0
    headers = ('ID', 'TITLE', 'PLACE', 'RELEASE', 'RATING', 'COUNTRIES')
    print('%-10s %-70s %-15s %-15s %-15s %-50s' % headers)
    try:
        response = get_popular()
    except Exception as e:
        print(f'Ошибка при выполнении запроса '
              f'GET /movie/popular: {e}')
    results = response.get('results')
    total_pages = response.get('total_pages')
    movies_counter = movie_info(results, movies_counter, n)
    for page_number in range(2, total_pages + 1):
        try:
            response = get_popular(page_number)
        except Exception as e:
            print(f'Ошибка при выполнении запроса '
                  f'GET /movie/popular: {e}')
        page_results = response.get('results')
        movies_counter = movie_info(page_results, movies_counter, n)


def main(args):
    if args.movies:
        show_movies(args.movies)
    else:
        show_actors(args.actors)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--movies', type=int, help='Enter number of movies')
    parser.add_argument('--actors', type=int, help='Enter movie id')
    args = parser.parse_args()
    main(args)
