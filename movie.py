import re, requests, sopel

API_KEY='' # TODO - Bot Config file

@sopel.module.commands('movie', 'imdb')
def movie(bot, trigger):
    """
    Returns some information about a movie, like Title, Year, Rating, Genre and IMDB Link.
    """
    if not trigger.group(2):
        return
    word = trigger.group(2).rstrip()
    uri = "https://api.themoviedb.org/3/search/movie"
    data = requests.get(uri, params={'api_key': API_KEY, 'query': word}, timeout=30).json()

    if len(data['results']) == 0:
        try:
            LOGGER.warning(
                'Got an error from TMDb: {}; data was {}'.format(word, str(data)))
            # this will fuck up
            message = "[MOVIE] Got an error from TMDb: {}".format(data['status_message'])
        except KeyError as err:
            message = "[MOVIE] Couldn\'t find {}".format(word)
    else:
        # Another request is made with TMDb's ID for the movie
        # If we've made it this far then there \shouldn't\ be any errors
        result_pos = 0
        for position in range(0, len(data['results'])):
            movie = data['results'][position]['original_title']
            m = re.search(r'{}$'.format(word), movie)
            if m:
                result_pos = position
                break

        id_search_url = "https://api.themoviedb.org/3/movie/{}"
        movie = requests.get(id_search_url.format(data['results'][result_pos]['id']),
                                params={'api_key': API_KEY}, timeout=30).json()

        message = '{} ({}) Rating: {} — http://imdb.com/title/{} — {}'.format(
                movie['original_title'], movie['release_date'], movie['vote_average'],
                movie['imdb_id'], movie['overview'])
    bot.say(message)

