import os
import tensorflow
import tensorflow.keras
from tensorflow import keras
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
from pyfiglet import Figlet
import pickle


def import_model():
    '''imports the model creates in train_model.py, reverse_mapping and
       sequences_array'''
    name = "dummy"  # otherwise loop does not start
    name = input("\nPlease enter the name of the artist you want to predict a concert setlist for. Press 'Enter' to finish:\n\n ")
    name = name.lower().strip().replace(' ', '-').replace('+', '_')
    model = keras.models.load_model((name + "_model"))
    with open(name + '_reverse_mapping', "rb") as file:
        reverse_mapping = pickle.load(file)
    with open(name + '_sequences_array', "rb") as file:
        sequences_array = pickle.load(file)
    return model, reverse_mapping, sequences_array


def create_reverse_mapping(mapping):
    '''Creates a reverse mapping to get back the song titles'''
    reverse_mapping = {v:k for k,v in mapping.items()}


def generate_full_setlist(model, seed_setlist, n_songs):
    '''Takes a length 50 np array of previous songs and generates complete next setlist'''
    setlist = []
    for _ in range(n_songs):
        # truncate the sequences
        seq = pad_sequences([seed_setlist], maxlen=50, truncating='pre')[0]
        # predict the next song
        next_song = np.argmax(model.predict(np.array([seq])), axis=-1).item()
        # applying reverse maping to get the actual song name
        next_song_ue = reverse_mapping[next_song]
        # append to list
        setlist.append(next_song_ue)
        # update seed_setlist
        seed_setlist = np.append(seed_setlist, next_song)
    return setlist


if __name__ == '__main__':
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' # suppresses messgaes from tf
    print(Figlet().renderText('PREDICT A CONCERT SETLIST\n'))
    model, reverse_mapping, sequences_array = import_model()
    seq = sequences_array[-1][1:]
    setlist = generate_full_setlist(model, seq, 25)
    print("\n\nHere's a possible setlist:\n\n")
    no = 1
    for i in setlist:
        print(str(no) + '. ' + i)
        no = no + 1
