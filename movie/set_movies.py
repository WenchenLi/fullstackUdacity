from movie import Movie
from fresh_tomatoes import *

#init instances of Movie
forrest_gump = Movie("https://upload.wikimedia.org/wikipedia/en/6/67/Forrest_Gump_poster.jpg",
                     "https://www.youtube.com/watch?v=8eCIRKJdV4k",
                     "Tom Hanks stars as the good hearted, but painfully slow Forrest Gump,"
                     " a man who manages to somehow be involved with almost every major event"
                     " in history during the last half of the 20th Century. Spanning the course "
                     "of his life,	the story follows him as he grows from a weak child to a war "
                     "hero to a shrimp boat captain, all the while pining for the love of his "
                     "childhood friend Jenny, played by Robin Wright.",
                     "Forrest Gump")

jobs = Movie("https://upload.wikimedia.org/wikipedia/en/e/e0/Jobs_%28film%29.jpg",
             "https://www.youtube.com/watch?v=GMZcdVCArRo",
             "Ashton Kutcher starts Steve Jobs, the iconic Apple innovator and groundbreaking"
             " entrepreneur. This inspiring and entertaining film chronicles Jobs' early"
             " days as a college dropout to his rise as the co-founder of Apple Computer "
             "Inc. and forced departure from the company. More than a decade later, Jobs "
             "returns and single-handedly sets a course that will turn the once-tiny "
             "startup into one of the world's most valuable companies. His epic journey "
             "blazes a trail that changes technology -- and the world -- forever. "
             "JOBS is a riveting story of a true American visionary, a man who let nothing "
             "stand in the way of greatness. Co-starring Dermot Mulroney, "
             "Josh Gad, J. K. Simmons and Matthew Modine.",
             "Jobs")

titanic = Movie("https://upload.wikimedia.org/wikipedia/en/2/22/Titanic_poster.jpg",
                "https://www.youtube.com/watch?v=2e-eXJ6HgkQ",
                "Leonardo DiCaprio and Oscar-nominatee Kate Winslet light up the screen "
                "as Jack and Rose, the young lovers who find one another on the maiden "
                "voyage of the \"unsinkable\" R.M.S. Titanic. But when the doomed luxury "
                "liner collides with an iceberg in the frigid North Atlantic, their passionate "
                "love affair becomes a thrilling race for survival. From acclaimed filmmaker "
                "James Cameron comes a tale of forbidden love and courage in the face of "
                "disaster that triumphs as a true cinematic masterpiece.",
                "Titanic")

# appending instances to movie list
movies = [forrest_gump, jobs, titanic]
# create webpage given movie list
create_movie_tiles_content(movies)
# open default browser to display
open_movies_page(movies)
