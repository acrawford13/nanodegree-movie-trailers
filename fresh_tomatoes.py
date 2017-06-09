import webbrowser
import os
import re


# Styles and scripting for the page
main_page_head = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Fresh Tomatoes!</title>
    <!-- Bootstrap 3 -->
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap-theme.min.css">
    <script src="http://code.jquery.com/jquery-1.10.1.min.js"></script>
    <script src="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/js/bootstrap.min.js"></script>
    <link href="https://fonts.googleapis.com/css?family=Roboto:400|Roboto+Condensed:700" rel="stylesheet">
    
    <style type="text/css" media="screen">
        body {
            padding-top: 80px;
            font-family: Roboto;
            color: #222222;
        }
        h2 {
            font-family: 'Roboto Condensed',sans-serif;
            font-size: 3.5rem;
            color: #00bcd4;
            margin-top: 0;
        }
        .container {
            max-width: 1050px;
        }
        .navbar-brand {
            font-family: 'Roboto Condensed',sans-serif;
            text-shadow: none;
        }
        .navbar-inverse .navbar-brand{
            color: #ddd;
        }
        #trailer .modal-dialog {
            margin-top: 150px;
            width: 640px;
            height: 480px;
        }
        .hanging-close {
            position: absolute;
            top: -12px;
            right: -12px;
            z-index: 9001;
        }
        #trailer-video {
            width: 100%;
            height: 100%;
        }
        button.trailer-button {
            padding :0.5rem 1rem;
            margin-top: 1rem;
            background-color: #607D8B;
            border: none;
            border-radius: 4px;
            color: white;
            font-family: 'Roboto',sans-serif;
            transition: background-color 0.4s;
        }
        button.trailer-button:hover {
            background-color: #455a64;
        }
        .genres {
            margin-bottom: 1rem;
        }
        .genres span {
            display: inline-block;
            padding: 0.2rem 0.7rem;
            margin: 0.2rem;
            background-color: #eeeeee;
            border: 0.5px solid #cccccc;
            border-radius: 1.2rem;
            color: #444444;
            font-size: 1.25rem;
        }
        .movie-tile {
            padding-bottom: 2rem;
        }
        .movie-tile .movie-poster, .movie-tile .movie-description {
            margin-bottom: 1rem;
        }
        footer {
            background-color:#222;
            padding: 1rem;
            text-align: right;
        }
        .scale-media {
            padding-bottom: 56.25%;
            position: relative;
        }
        .scale-media iframe {
            border: none;
            height: 100%;
            position: absolute;
            width: 100%;
            left: 0;
            top: 0;
            background-color: white;
        }
            
    </style>
    <script type="text/javascript" charset="utf-8">
        // Pause the video when the modal is closed
        $(document).on('click', '.hanging-close, .modal-backdrop, .modal', function (event) {
            // Remove the src so the player itself gets removed, as this is the only
            // reliable way to ensure the video stops playing in IE
            $("#trailer-video-container").empty();
        });
        // Start playing the video whenever the trailer modal is opened
        $(document).on('click', '.movie-tile .trailer-button', function (event) {
            var trailerYouTubeId = $(this).attr('data-trailer-youtube-id')
            var sourceUrl = 'http://www.youtube.com/embed/' + trailerYouTubeId + '?autoplay=1&html5=1';
            $("#trailer-video-container").empty().append($("<iframe></iframe>", {
              'id': 'trailer-video',
              'type': 'text-html',
              'src': sourceUrl,
              'frameborder': 0
            }));
        });
        // Animate in the movies when the page loads
        $(document).ready(function () {
          $('.movie-tile, footer').hide().first().fadeIn("fast", function showNext() {
            if($(this).next("div")[0]){
              $(this).next("div").fadeIn("fast", showNext);
            } else {
              $('footer').fadeIn("fast");
            }
          });
        });
	
    </script>
</head>
'''


# The main page layout and title bar
main_page_content = '''
  <body>
    <!-- Trailer Video Modal -->
    <div class="modal" id="trailer">
      <div class="modal-dialog">
        <div class="modal-content">
          <a href="#" class="hanging-close" data-dismiss="modal" aria-hidden="true">
            <img src="https://lh5.ggpht.com/v4-628SilF0HtHuHdu5EzxD7WRqOrrTIDi_MhEG6_qkNtUK5Wg7KPkofp_VJoF7RS2LhxwEFCO1ICHZlc-o_=s0#w=24&h=24"/>
          </a>
          <div class="scale-media" id="trailer-video-container">
          </div>
        </div>
      </div>
    </div>

    <!-- Main Page Content -->
    <div class="container">
      <div class="navbar navbar-inverse navbar-fixed-top" role="navigation">
        <div class="container">
          <div class="navbar-header">
            <a class="navbar-brand" href="#">Fresh Tomatoes Movie Trailers</a>
          </div>
        </div>
      </div>
    </div>
    <div class="container">
      {movie_tiles}
    </div>
    <footer>
        <div class="container">
            <a href="https://www.themoviedb.org/" target="_blank"><img height="50" src="https://www.themoviedb.org/assets/static_cache/9b3f9c24d9fd5f297ae433eb33d93514/images/v4/logos/408x161-powered-by-rectangle-green.png" alt="Powered by The Movie DB"></a>
        </div>
    </footer>
  </body>
</html>
'''


# A single movie entry html template
movie_tile_content = '''
<div class="row movie-tile">
  <div class="col-xs-6 col-xs-push-3 col-sm-push-0 col-sm-3 col-md-2 movie-poster">
    <img src="{poster_image_url}" width="100%">
  </div>
  <div class="col-xs-12 col-sm-9 col-md-10 movie-description">
    <h2>{movie_title}</h2>
    <div class="genres">{genres}</div>
    <p>{storyline}</p>
    <button class="trailer-button" data-trailer-youtube-id="{trailer_youtube_id}" data-toggle="modal" data-target="#trailer">Watch trailer</button>
  </div>
</div>
'''

def create_movie_tiles_content(movies):
    # The HTML content for this section of the page
    content = ''
        
    for movie in movies:
        # Extract the youtube ID from the url
        youtube_id_match = re.search(
            r'(?<=v=)[^&#]+', movie.trailer_youtube_url)
        youtube_id_match = youtube_id_match or re.search(
            r'(?<=be/)[^&#]+', movie.trailer_youtube_url)
        trailer_youtube_id = (youtube_id_match.group(0) if youtube_id_match
                              else None)
        
        # Loop through the movie genres and construct the HTML content
        genre_content = ''
        genre_format = "<span>{0}</span>"
        for genre in movie.genres:
            genre_content += genre_format.format(genre)
            
        # Append the tile for the movie with its content filled in
        content += movie_tile_content.format(
            movie_title=movie.title,
            poster_image_url=movie.poster_image_url,
            trailer_youtube_id=trailer_youtube_id,
            storyline=movie.storyline.encode('utf-8'),
            genres=genre_content
        )
        
    return content


def open_movies_page(movies):
    # Create or overwrite the output file
    output_file = open('fresh_tomatoes.html', 'w')

    # Replace the movie tiles placeholder generated content
    rendered_content = main_page_content.format(
        movie_tiles=create_movie_tiles_content(movies))

    # Output the file
    output_file.write(main_page_head + rendered_content)
    output_file.close()

    # open the output file in the browser (in a new tab, if possible)
    url = os.path.abspath(output_file.name)
    webbrowser.open('file://' + url, new=2)
