__author__ = 'MBA11'
import MovieList


def create_list_from_file(file) -> list:
    """function to open a text file and retrieve every line and turn it into an element of a list
    :param file:
    :rtype: list"""
    line_number = 0
    new_list = []
    file_data = open(file).readlines()
    while line_number < len(file_data):
        if file_data[line_number] != '\n':
            new_list.append(file_data[line_number].strip())
        line_number += 1
    return new_list


def format_movie_list() -> str:
    """
    function to strip out all irrelevant data in json movieData
    :rtype : str
    """
    # read from file into string
    with open("movieData", "r") as rawMovieDataFile:
        movieDataStringRaw = rawMovieDataFile.read().replace('\n', '')
    # manipulate string to be formatted correctly

    formatted_movie_data = ""
    counter = 0
    temp_word = ""
    writing_to_format = False
    while counter < len(movieDataStringRaw):
        c = movieDataStringRaw[counter]
        if c == '{':
            formatted_movie_data += c
            formatted_movie_data += '\n'
            counter += 1
            continue
        if c == '}' and formatted_movie_data[len(formatted_movie_data) - 1] != '{':
            formatted_movie_data = formatted_movie_data[:-2]
            formatted_movie_data += '\n'
            formatted_movie_data += c
            formatted_movie_data += '\n'
            counter += 1
            continue
        if writing_to_format is True:
            formatted_movie_data += c
        if writing_to_format is False:
            temp_word += c

        if writing_to_format is False:
            if "\"Title\":" in temp_word:
                formatted_movie_data += '\t'
                formatted_movie_data += temp_word[-len("\"Title\":"):]
                writing_to_format = True
                temp_word = ""
            elif "\"Year\":" in temp_word:
                formatted_movie_data += '\t'
                formatted_movie_data += temp_word[-len("\"Year\":"):]
                writing_to_format = True
                temp_word = ""
            elif "\"Genre\":" in temp_word:
                formatted_movie_data += '\t'
                formatted_movie_data += temp_word[-len("\"Genre\":"):]
                writing_to_format = True
                temp_word = ""
            elif "\"Plot\":" in temp_word:
                formatted_movie_data += '\t'
                formatted_movie_data += temp_word[-len("\"Plot\":"):]
                writing_to_format = True
                temp_word = ""
            elif "\"tomatoMeter\":" in temp_word:
                formatted_movie_data += '\t'
                formatted_movie_data += temp_word[-len("\"tomatoMeter\":"):]
                writing_to_format = True
                temp_word = ""
            elif "\"tomatoUserMeter\":" in temp_word:
                formatted_movie_data += '\t'
                formatted_movie_data += temp_word[-len("\"tomatoUserMeter\":"):]
                writing_to_format = True
                temp_word = ""
        if writing_to_format is True and c == ',' and movieDataStringRaw[counter - 1] == '\"':
            formatted_movie_data += '\n'
            writing_to_format = False
        counter += 1
    return formatted_movie_data


print("started...")

# create a list from a file of movie titles
titlesFromTxt = create_list_from_file('movieTitleList')
print("extracted titles from text file...")

#create a MovieList object to perform appropriate operations
list_of_movies = MovieList.MovieList(titlesFromTxt)
print("create MovieList object...")

#trim the year off the title if necessary
list_of_movies.trim_title_of_year_and_replace_spaces()
print("annotated titles...")

#sort alphabetically and remove duplicates
list_of_movies.sort_and_rem_duplicate_titles()
print("cleaned up list...")

for movie in list_of_movies.titles:
    print(movie)

#fetch data from omdb and RT api and create an array of json objects with the movie property fields
print("fetching data from internet...")
list_of_movies.create_movies_json('movieData')
print("created json file...")


# Now we need to clean up the json file for each json movie object
# The format we want the json movie object to be in will then be
# written to the 'formattedMovieData' which then can be amended to the
# 'MasterFinalList' file manually after final human inspection

# json object format:
# Title (1), Year (2), Genre (6), Plot(10), tomatoMeter(20), tomatoUserMeter(27)
# I no longer know what the numbers in the () indicate, but will leave them in case
# I need them for anything in the future

formatted_data = format_movie_list()
print(formatted_data)
f = open('formattedMovieData', "w")
f.write(formatted_data)
f.close()
print(formatted_data.count("\"Title\":"))
