from __future__ import print_function
import re, requests, os

API_KEY_PATH = '~/.tmdb'
BASE_URL = 'https://api.themoviedb.org/3/search/multi?api_key={}&query={}'

def movie_lookup(api_key, title):
    """
    Returns some information about a movie or TV show, like Title, Year, Rating, Genre and IMDB Link.
    """
    query = requests.get(BASE_URL.format(api_key, title)).json()
    if 'results' not in query or not query:
        return None
    elif len(query['results']) == 0:
        return None
    else:
        id_search_url = "https://api.themoviedb.org/3/{}/{}?api_key={}"
        info = requests.get(id_search_url.format(
                                                query['results'][0]['media_type'],
                                                query['results'][0]['id'],
                                                api_key)).json()
        if query['results'][0]['media_type'] == 'movie':
            response = '{} ({}) Rating: {} —https://imdb.com/title/{} —{}'.format(
                                                 info['original_title'],
                                                 info['release_date'],
                                                 info['vote_average'],
                                                 info['imdb_id'],
                                                 info['overview'])
            return response
        else:
            response = '{} ({}) Rating: {} Episodes: {} —{}'.format(
                                                info['original_name'],
                                                info['first_air_date'],
                                                info['vote_average'],
                                                info['episode_run_time'][0],
                                                info['overview'])
            return response


try:
    import sopel.module
except ImportError:
    # Probably running from commandline
    pass
else:
    @sopel.module.commands('movie', 'imdb', 'tmdb')
    @sopel.module.example('.movie The Martian')
    def f_movie_lookup(bot, trigger):
        """Look up the details of a movie in TMDB"""
        if trigger.group(2):
            api_key = open(os.path.expanduser(API_KEY_PATH), 'r').read().strip()
            # api_key = bot.config.tmdb.api_key
            query = re.sub('[^a-zA-Z ]', '', trigger.group(2)).strip()
            details = movie_lookup(api_key, query)
            if details is not None:
                bot.say(details, trigger.sender, len(details)*2)
            else:
                bot.say('Couldn\'t find anything for "{}".'.format(query), trigger.sender)
        return sopel.module.NOLIMIT

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
        details = movie_lookup(api_key, query)
        if details is not None:
            print(details)
        else:
            print('Couldn\'t find anything for "{}"'.format(query))
