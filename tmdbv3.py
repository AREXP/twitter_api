import argparse

from api import (get_movie_cast, get_movie_detail, get_person_detail,
                 get_popular, get_top_rated)

PAGE_SIZE = 20
NUMBER_OF_ACTORS = 5


def search_film_position_in_page(movie_id, movies):
    for position, movie in enumerate(movies, start=1):
        if movie['id'] == movie_id:
            return position


def get_place_in_rate(movie_id):
    total_pages = get_top_rated().get('total_pages')
    for page_number in range(1, total_pages + 1):
        movies = get_top_rated(page_number).get('results')
        position_on_page = search_film_position_in_page(movie_id, movies)
        if position_on_page and page_number == 1:
            return position_on_page
        elif position_on_page and page_number > 1:
            return page_number * PAGE_SIZE + position_on_page
    return 0


def get_production_countries(movie_id):
    production_countries = get_movie_detail(movie_id).get(
        'production_countries')
    return ', '.join([pc.get('iso_3166_1') for pc in production_countries])


def movie_info(movie):
    movie_id = movie.get('id')
    title = movie.get('title')
    release_date = movie.get('release_date')
    rating = movie.get('vote_average')
    place_in_rate = get_place_in_rate(movie_id)
    production_countries = get_production_countries(movie_id)
    print(f'{movie_id:<10} {title:<50} {place_in_rate:<15} {release_date:<15} '
          f'{rating:<15} {production_countries:<50}')


def movie_cast_info(movie_id):
    headers = ('NAME', 'CHARACTER', 'BIRTHDAY', 'PLACE_OF_BIRTH')
    print('%-40s %-40s %-15s %-50s' % headers)
    movie_cast = get_movie_cast(movie_id)
    actors = []
    for cast in movie_cast:
        if cast['known_for_department'] == 'Acting':
            actors.append(cast)
    for actor in actors[:NUMBER_OF_ACTORS]:
        actor_id = actor.get('id')
        name = actor.get('name')
        character = actor.get('character')
        actor_info = get_person_detail(actor_id)
        birthday = actor_info.get('birthday')
        place_of_birth = actor_info.get('place_of_birth')
        print('-' * 140)
        print(
            f'{name:<40} {character:<40} {birthday:<15} {place_of_birth:<50}'
        )


def movies(n):
    movies_counter = 0
    headers = ('ID', 'TITLE', 'PLACE', 'RELEASE', 'RATING', 'COUNTRIES')
    print('%-10s %-50s %-15s %-15s %-15s %-50s' % headers)
    total_pages = 1
    for page_number in range(1, total_pages + 1):
        popular_response = get_popular(page_number)
        total_pages = popular_response.get('total_pages')
        popular_movies = popular_response.get('results')
        for movie in popular_movies:
            if movies_counter < n:
                print('-' * 140)
                movie_info(movie)
                movies_counter += 1
            else:
                exit()


def main(args):
    if args.movies:
        movies(args.movies)
    else:
        movie_cast_info(args.actors)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--movies', type=int, help='Enter number of movies')
    parser.add_argument('--actors', type=int, help='Enter movie id')
    args = parser.parse_args()
    main(args)
