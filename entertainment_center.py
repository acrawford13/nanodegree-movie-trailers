import media
import fresh_tomatoes

serenity = media.Movie("tt0379786", "https://www.youtube.com/watch?v=JY3u7bB7dZk")
rogueone = media.Movie("tt3748528", "https://www.youtube.com/watch?v=frdj1zb9sMY")
nocountry = media.Movie("tt0477348", "https://www.youtube.com/watch?v=38A__WT3-o0")
vforvendetta = media.Movie("tt0434409", "https://www.youtube.com/watch?v=qxyUl9M_7vc")
bluesbrothers = media.Movie("tt0080455", "https://www.youtube.com/watch?v=2HCR4c1zPyk")
seriousman = media.Movie("tt1019452", "https://www.youtube.com/watch?v=mDKHWRbK2_Q")

movies = [seriousman, bluesbrothers, nocountry, rogueone, serenity, vforvendetta]

fresh_tomatoes.open_movies_page(movies)
