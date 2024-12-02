import streamlit as st # type: ignore
import pickle
import pandas as pd
import requests
from dotenv import load_dotenv

movies_dict=pickle.load(open('movie_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)
ndf=movies
load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")
def fetch_poster(id):
    url = f"https://api.themoviedb.org/3/movie/{id}?api_key={API_KEY}&language=en-US"
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def arr_to_tuplist(obj):
  A=[]
  for x in range(len(obj)):
    A.append((obj[x],x))
  return A

cs=pickle.load(open('similarity_mat.pkl','rb'))

def recomend(movie):
  indx=ndf[ndf['title']==movie].index[0]   # index
  distance=cs[indx]
  movie_id=ndf['movie_id'].loc[indx]
  A=arr_to_tuplist(distance)
  #a  -> { similiarity score , index }
  a=sorted(A,reverse=True)
  #print(a)
  #print(a[0][0])
  rec=[]
  pos=[]
  for i in range (1,6):
      
      rec.append(ndf['title'].loc[a[i][1]])
      pos.append(fetch_poster(ndf['movie_id'].loc[a[i][1]]))
  return rec, pos
    


st.title('Movie  Recommender System')
import streamlit as st # type: ignore
option = st.selectbox(
    "Select A Movie",
    movies['title'].values)
# st.write("You selected:", option)



if st.button('Search'):
    recommended_movie_names,recommended_movie_posters = recomend(option)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])
