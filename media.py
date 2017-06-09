import requests
import json
import passwords


class Movie():
    """ This class provides a way to store movie-related information.
    
    Args:
        imdb_id (str): IMDb ID
        youtube_trailer_url (str): YouTube Trailer URL
    """
    
    # API Key for The Movie DB - https://www.themoviedb.org/faq/api
    API_KEY = passwords.API_KEY

    # Get image url from API (see below for correct image url format)
    # https://developers.themoviedb.org/3/getting-started/images
    url = "https://api.themoviedb.org/3/configuration?api_key=" + API_KEY
    response = requests.request("GET", url)
    IMAGE_URL = json.loads(response.text)['images']['base_url']
    POSTER_SIZE = "w342"

    # Get list of genre ids
    url = "https://api.themoviedb.org/3/genre/movie/list?api_key="
    url += API_KEY + "&language=en-US"
    response = requests.request("GET", url)
    genres = json.loads(response.text)['genres']

    # Change format of genre response so we can fetch the genre name by its ID
    GENRES = {}
    for genre in genres:
        GENRES[genre['id']] = genre['name']

    def __init__(self, imdb_id, youtube_trailer_url):
        # Construct the URL for the request
        url = "https://api.themoviedb.org/3/find/" + imdb_id
        url += "?api_key=" + Movie.API_KEY
        url += "&language=en-US&external_source=imdb_id"
        
        # Store response and convert to a dictionary
        response = requests.request("GET", url)
        response = json.loads(response.text)

        # Generate list of genre names from genre ids
        self.genres = []
        for genre_id in response['movie_results'][0]['genre_ids']:
            self.genres.append(Movie.GENRES[genre_id].encode('utf-8'))

        # assign reponses to instance properties
        self.title = response['movie_results'][0]['title']
        self.storyline = response['movie_results'][0]['overview']
        self.poster_image_url = Movie.IMAGE_URL + Movie.POSTER_SIZE
        self.poster_image_url += response['movie_results'][0]['poster_path']
        self.trailer_youtube_url = youtube_trailer_url
