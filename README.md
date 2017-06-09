# Fresh Tomatoes Movie Trailer Website Project
Source code for a Movie Trailer website using the [Movie DB API](https://www.themoviedb.org/documentation/api).

## Getting Started
- You will need an API key from The Movie DB ([More info](https://www.themoviedb.org/faq/api))
- Replace the `API_KEY` variable with your own key on line 15 of `media.py` or create your own `passwords.py` file containing the variable `API_KEY`
- Requires [requests](http://docs.python-requests.org/en/master/) package

## Adding/Removing a Movie
- You can add or remove movies in the `entertainment_center.py` file
- Create a movie instance using `newmovie = media.Movie("<IMDb ID>","<YouTube Trailer URL>")`. (The IMDb ID is displayed in the IMDb URL, eg.: http://www.imdb.com/title/tt0245429, ID = "tt0245429")
- Make sure you add the new movie to the `movies` list

## License
This project is licensed under the terms of the [MIT license](https://opensource.org/licenses/MIT).
