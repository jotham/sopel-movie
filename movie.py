from __future__ import print_function
import re, requests, os

API_KEY_PATH = '~/.tmdb'
BASE_URL = 'https://api.themoviedb.org/3/search/multi?api_key={}&query={}'

def imdb_search(api_key, title):
    """
    Returns some information about a movie or TV show, like Title, Year, Rating, Genre and IMDB Link.
    """
    query = requests.get(BASE_URL.format(api_key, title)).json()
    if 'results' not in query or not query:
        return None
    elif query['results'] == 0:
        return None
    else:
        id_search_url = "https://api.themoviedb.org/3/{}/{}?api_key={}"
        info = requests.get(id_search_url.format(query['results'][0]['media_type'],
                                                query['results'][0]['id'],
                                                 api_key)).json()
        if query['results'][0]['media_type'] is 'movie':
            return [info['original_title'], info['release_date'], info['vote_average'],
                    'https://imdb.com/title/' + info['imdb_id'], info['overview']]
        else:
            return [info['original_name'], info['first_air_date'], info['vote_average'],
                    'Episodes: ' + str(info['episode_run_time'][0]), info['overview']]


try:
    import sopel.module
except ImportError:
    # Probably running from commandline
    pass
else:
    @sopel.module.commands('imdb')
    @sopel.module.example('.imdb The Martian')
    def f_imdb(bot, trigger):
        query = trigger.group(2).strip()
        results = imdb_search(bot.config.tmdb.api_key, query)
        bot.say(imdb_search(query))


if __name__ == '__main__':
    import sys
    try:
        api_key = open(os.path.expanduser(API_KEY_PATH), 'r').read().strip()
    except FileNotFoundError:
        print('Can\'t get API key in ' + API_KEY_PATH)
        sys.exit(1)
    else:
        query = 'The Martian'
        if len(sys.argv) > 1:
            query = ' '.join(sys.argv[1:])
        print('Looking up "{}"'.format(query))
        results = imdb_search(api_key, query)
        if results:
            print('{} ({}) Rating: {} —{} —{}'.format(*results))
        else:
            print('Couldn\'t find anything for "{}"'.format(query))
