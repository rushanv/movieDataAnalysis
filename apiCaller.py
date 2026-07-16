import pandas as pd
import requests as rq
from dotenv import load_dotenv
import os

load_dotenv()

OMDBAPI_KEY = os.getenv("OMDBAPI_KEY")


def compile_movies(movie_info_array):
    movie_df = pd.read_csv("moviedata/movies.csv")
    num_movies = len(movie_info_array)
    num_success = 0
    if len(movie_info_array[0]) == 2:
        for name, year in movie_info_array:
            if movie_df.isin([name]).sum().get("Title") == 0:
                data = rq.get(f"http://www.omdbapi.com/", params={"apikey": OMDBAPI_KEY, "t": name, "y": str(int(year))}).json()
                if data["Response"] == "True":
                    df = pd.DataFrame([data])
                    df_array = df.to_numpy()
                    if df_array[0][2] != "N/A":
                        df_array[0][0] = name
                        df = pd.DataFrame(df_array)
                        df.to_csv("moviedata/movies.csv", mode="a", header=False, index=False)
                        num_success += 1
    else:
        for name in movie_info_array:
            if movie_df.isin([name]).sum().get("Title") == 0:
                data = rq.get(f"http://www.omdbapi.com/", params={"apikey": OMDBAPI_KEY, "t": name}).json()
                if data["Response"] == "True":
                    df = pd.DataFrame([data])
                    df_array = df.to_numpy()
                    if df_array[0][2] != "N/A":
                        df_array[0][0] = name
                        df = pd.DataFrame(df_array)
                        df.to_csv("moviedata/movies.csv", mode="a", header=False, index=False)
                        num_success += 1

    print(f"{num_success}/{num_movies} movies successfully saved")
    return True

def compile_mov_from_ratings():
    rating_df = pd.read_csv("moviedata/ratings.csv")[["Name", "Year"]]
    rating_array = rating_df.to_numpy()
    compile_movies(rating_array)

def compile_movie(movie):
    compile_movies([movie])

# t_movie = [["Her", 2013.0]]
# compile_movies(t_movie)
# data = rq.get(f"http://www.omdbapi.com/", params={"apikey": OMDBAPI_KEY, "t": "Her", "y": str(int(2013.0))}).json()
# print(data)
