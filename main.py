import numpy as np
import pandas as pd
import colorama
import threading
import concurrent.futures


colorama.init()

print("loading files...\n")

#cosine_sim = np.load("sim.npy")

def load_matrix():
    cosine_sim = np.load("sim.npy")
    return cosine_sim


def get_song_id(inp_str):
    ids = pd.read_csv("id.csv")
    mask = ids["search"].str.contains(inp_str, regex=False, case=False)
    search_results = ids[mask]
    for i in range(len(search_results)):
        song_id = search_results.iloc[i, 0]
        song_name = search_results.iloc[i, 1]
        song_artist = search_results.iloc[i, 2]
        if(song_id < 40001):
            print(str(song_id) + "\t" + song_name + " by " + song_artist)
            print("\n")

    song_id = int(input("Enter song ID: "))
    return song_id


def get_recommendations(idx, cosine_sim):
    
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the songs based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the 10 most similar songs
    sim_scores = sim_scores[1:11]
    sim_scores.sort()
    # Get the song indices
    song_index = [i[0] for i in sim_scores]
    song_index = song_index
    # Return the top 10 most similar songs
    return song_index

def display_recoms(recoms, idx):
    song_id = pd.read_csv("id.csv")
    print("Song recommendations for: " + song_id.iloc[idx, song_id.columns.get_loc("name")]+" by " + song_id.iloc[idx, song_id.columns.get_loc("artists")])
    for i in recoms:
        print(song_id.iloc[i, song_id.columns.get_loc("name")] + " by " +\
            song_id.iloc[i, song_id.columns.get_loc("artists")])
        print("\n")



def main():
    # matrix = threading.Thread(target=load_matrix).start()
    # inp_str = input("Enter song name: ")
    # song_id = get_song_id(inp_str)
    # recomms = get_recommendations(song_id, matrix)
    # display_recoms(recomms, song_id)
    # print('\n')

    with concurrent.futures.ThreadPoolExecutor() as exec:
        loader = exec.submit(load_matrix)
        matrix = loader.result()
        inp_str = input("Enter song name: ")
        song_id = get_song_id(inp_str)
        recomms = get_recommendations(song_id, matrix)
        display_recoms(recomms, song_id)


main()