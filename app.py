import streamlit as st
import pickle
import pandas as pd
import requests
import gdown
import os



def fetch_poster(id):
    data = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=e353f124c21c4fbeb34498dac2cb25b6&language=en-US'.format(id))
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path
def recommend(movie):
    movie_index=movies[movies['title' ]== movie].index[0]
    distances=similarity[movie_index]
    movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    recommended_movies=[]
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].id
        #fetch posters
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies,recommended_movies_posters
movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)
#similarity =  pickle.load(open('similarity.pkl','rb'))
# Google Drive File ID for similarity.pkl
#https://drive.google.com/file/d/1LsAz-AYCtsLXLj4RSvdGoOhhu6Bxeky6/view?usp=sharing
SIMILARITY_FILE_ID = "1LsAz-AYCtsLXLj4RSvdGoOhhu6Bxeky6"
SIMILARITY_FILE_PATH = "similarity.pkl"

# Download the file if it doesn’t exist
if not os.path.exists(SIMILARITY_FILE_PATH):
    gdown.download(f"https://drive.google.com/uc?id={SIMILARITY_FILE_ID}", SIMILARITY_FILE_PATH, quiet=False)

# Load the pickle file
similarity = pickle.load(open(SIMILARITY_FILE_PATH, "rb"))

st.title('Movie Recommender System')
selected_movie_name = st.selectbox('Welcome',movies['title'].values)

if st.button('Recommend'):
    names,posters = recommend(selected_movie_name)
    col1,col2,col3,col4,col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])