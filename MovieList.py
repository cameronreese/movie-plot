__author__ = 'Cameron Reese'


import json
from urllib.request import urlopen

class MovieList:
    """ This class contains the tools to take a list of movie titles and turn them into objects"""
    titles = [] # the start property of this class, a list of movie titles

# constructor for class, creates a class object that has a list of movie titles
    def __init__(self, list):
        self.titles = list

# function to trim the "(YYYY)" from the end of a movie title, making it in the proper
# format for OMDB api movie title syntax
    def trim_title_of_year_and_replace_spaces(self):
        i = 0
        while i < len(self.titles):
            if '(' in self.titles[i]:
                trimmed_title = self.titles[i][0:self.titles[i].index(" (")]
            trimmed_title = trimmed_title.replace(" ", "+")
            self.titles[i] = trimmed_title
            i += 1


# function to sort list and remove duplicate titles, this only modifies the 'titles[]'
    def sort_and_rem_duplicate_titles(self):
        self.titles = list(set(self.titles))
        self.titles.sort()

# fetch data from the omdb api and create a json obj of movies with the following properties:
#   Title, Year, Rated, Released, Runtime, Genre, Director, Writer, Actors, Plot, Language,
#   Country, Awards, Poster, Metascore, imbdRating, imdbVotes, imdbID, Type, tomatoMeter,
#   tomatoImage, tomatoRating, tomatoReviews, tomatoFresh, tomatoRotten, tomatoConsensus,
#   tomatoUserMeter, tomatoUserRating, tomatoUserReviews, DVD, BoxOffice, Production, Website, Response
    def create_movies_json(self, file):
        movie_data_str = ""
        counter = 0
        for item in self.titles:
            fetch = urlopen('http://www.omdbapi.com/?t=' + item + '&tomatoes=true')
            ind_movie_data = str(fetch.read())
            ind_movie_data = ind_movie_data[2:len(ind_movie_data)-1]
            if '\\' in ind_movie_data:
                ind_movie_data = ind_movie_data.replace("\\", "")
            movie_data_str = movie_data_str + ind_movie_data
            counter += 1
        print(counter)
        open(file, mode='w').write(movie_data_str)
