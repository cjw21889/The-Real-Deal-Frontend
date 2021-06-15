import json
import streamlit as st
from streamlit_tags import st_tags
import requests

model_url = "https://trdapi-2rnxcmyipa-ew.a.run.app/predict?"
st.header('The Real Deal - Netflix Ratings Predictions')
view = st.sidebar.selectbox('Choose View:', ['Movie Search', 'Movie Build', 'Future Releases'])


def display_movies(movie):
    poster = movie.get('Poster', 'image.jpg')
    if poster == 'N/A':
        poster = 'image.jpg'
    st.title(movie['Title'])
    col1, col2 = st.beta_columns(2)
    col1.image(poster)
    col2.write(f"Released: {movie['Year']}")
    col2.write(f"Runtime: {movie['Runtime']}")
    col2.write(f"Rated: {movie['Rated']}")
    col2.write(f"Genre: {movie['Genre']}")
    col2.write(f"Director: {movie['Director']}")
    col2.write(f"Writer: {movie['Writer']}")
    col2.write(f"Actors: {movie['Actors']}")
    col2.write(f"Language: {movie['Language']}")
    col2.write(f"Plot: {movie['Plot']}")

    model_params = {'runtime': movie['Runtime'],
                    'genre': movie['Genre'],
                    'year': movie['Year'],
                    'rated': movie['Rated'],
                    'director': movie['Director'],
                    'writer': movie['Writer'],
                    'actors': movie['Actors'],
                    'plot': movie['Plot'],
                    'language': movie['Language'],
                    'production': ['Production']
                    }
    response = requests.get(model_url, params=model_params).json()

    st.subheader(
        f"Predicted Netflix Rating: {round(response['prediction'],2)}")


if view == 'Movie Search':
    movie = st.text_input('Movie Title')
    if movie:
        imdb_url = f"http://www.omdbapi.com/?t={movie}&apikey=ef5507df"
        response = requests.get(imdb_url).json()

        with open('departed.json', 'r') as f:
            # json.dump(response, f)
            # movie = json.load(f)
            movie = response

            display_movies(movie)
    else:
        st.image('background.jpg')

if view == 'Movie Build':
    col1, col2 = st.beta_columns(2)
    runtime = col2.text_input("Runtime: ")
    rated = col2.text_input("Rated: ")
    genre = col2.multiselect('Pick a Genre', ['Horror', 'Comedy', 'Action', 'Romance',
                                     'Thriller', 'Adventure', 'Sci-Fi', 'Western'])
    language = col2.text_input(f"Language: ")
    director = col1.text_input(f"Director: ")
    writer = col1.text_input(f"Writer: ")
    actors = col1.text_input(f"Actors: ")
    production = col1.text_input(f"Production: ")
    plot = st.text_input(f"Plot: ")


    run = st.button('Rate my movie')
    if run:
        movie = {'Runtime': runtime,
                 'Title' : 'Unnamed Project',
                 'Genre': ', '.join(genre),
                 'Year': 2021,
                 'Rated': rated,
                 'Director': director,
                 'Writer': writer,
                 'Actors': actors,
                 'Plot': plot,
                 'Language': language,
                 'Production': production
                }
        display_movies(movie)

if view == 'Future Releases':
    movies = ['awake.json', 'cruella.json', 'wrong-turn.json']

    for mov in movies:
        with open(mov, 'r') as f:
            # json.dump(response, f)
            display_movies(json.load(f))



