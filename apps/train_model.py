import pandas as pd
import numpy as np
import time
import pickle
from pyfiglet import Figlet
import tensorflow
import tensorflow.keras
from sklearn.model_selection import train_test_split
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Embedding, Dropout, LSTM, Dense
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.preprocessing.sequence import pad_sequences


def load_artist_file():
    '''Loads the corresponding csv file and customizes the dataframe (drops rows)'''
    name = "dummy"  # otherwise loop does not start
    name = input("\nPlease enter the name of the artist you want to train a model for. Press 'Enter' to finish:\n\n ")
    name = name.lower().strip().replace(' ', '-').replace('+', '_')
    df_raw = pd.read_csv(name +'.csv', index_col=0)
    df_raw2 = df_raw[df_raw.concert_year != 2006]
    df = df_raw2[df_raw2.concert_year != 2007]
    return df, name


def create_setlist_string(df, name):
    '''
    * Creates a single string out of all song_list
    * Creates a list of all unique songs
    '''
    print('\n\nPreparing the corpus...\n\n')
    setlist_list = []
    for i, row in df.iterrows():
    # add ', ' unless its the last record
        if i == df.shape[0]-1:
            setlists = row.setlist
        else:
            setlists = row.setlist + ', '
    # append to list
        setlist_list.append(setlists)
    # join to one long string
    setlist_string = ''.join(setlist_list)
    setlist_string_list = setlist_string.split(', ')
    unique_songs = sorted(set(setlist_string_list))
    print(f'Not bad, there are {len(setlist_string_list)} {name} songs in this corpus.')
    print(f'{name} have {len(unique_songs)} unique songs.\n\n')
    return setlist_string_list, unique_songs


def create_mapping(unique_songs):
    '''Converts every song name in int'''
    mapping = {song:index for index, song in enumerate(unique_songs)}
    return mapping


def apply_mapping_to_corpus(setlist_string_list):
    '''Applies the above encoding to the full list of songs'''
    print('Encoding the song names...')
    encoded_setlist_string_list = ""
    encoded_setlist_string_list = [mapping[song] for song in setlist_string_list]
    print(f'Encoded all {len(encoded_setlist_string_list)} songs in the corpus!\n\n')
    return encoded_setlist_string_list


def creating_sequences_for_model(encoded_setlist_string_list):
    '''Creates sequences of length 50 to give the model and appends them to list'''
    length = 50
    sequences = []
    for i in range(length, len(encoded_setlist_string_list)):
        seq = encoded_setlist_string_list[i-length: i+1]
    # append to list
        sequences.append(seq)
    sequences_array = np.array(sequences)
    print(f'Created {len(sequences)} sequences for the model.\n\n')
    return sequences_array


def create_X_y(sequences_array):
    '''Creates X and y data and does train_test_split'''
    print('Defining X and y data...\n\n')
    X_data, y_data = sequences_array[:,:-1], sequences_array[:,-1]
    X_train, X_test, y_train, y_test = train_test_split(X_data, y_data, test_size=0.2, random_state=2)
    return X_train, X_test, y_train, y_test


def one_hot_encode(unique_songs):
    '''One hot encodes the y data and counts unique songs'''
    num_classes = len(unique_songs)
    y_train_hot = to_categorical(y_train, num_classes=num_classes)
    y_test_hot = to_categorical(y_test, num_classes=num_classes)
    return y_train_hot, y_test_hot, num_classes


def train_model(num_classes):
    '''Trains a neural network with defined parameters'''
    print('Finally...training the model...\n\n')
    model = Sequential([
        Embedding(input_dim=num_classes, output_dim=150, input_length=50),
        Dropout(0.5),
        LSTM(units=100, recurrent_dropout=0.5),
        #Dropout(0.5),
        Dense(units=50, activation='relu'),
        Dense(units=num_classes, activation='softmax')
        ])
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    callback = EarlyStopping(monitor='val_loss', patience=3)
    history = model.fit(X_train, y_train_hot, batch_size=500, epochs=100, callbacks=[callback], validation_split=0.2)
    return model


def evaluating_model(model):
    ''''Evaluates the model by printing accuracy and loss'''
    loss, accuracy = model.evaluate(X_train, y_train_hot)
    print(f' The accuracy is {accuracy}.\n\n' )
    print(f' The loss is {loss}.\n\n')
    return accuracy, loss


if __name__ == '__main__':
    print(Figlet().renderText('Train a\n Setlist Predictor\n'))
    df, name = load_artist_file()
    setlist_string_list, unique_songs = create_setlist_string(df, name)
    mapping = create_mapping(unique_songs)
    reverse_mapping = {v:k for k,v in mapping.items()}
    with open(name + '_reverse_mapping', "wb") as file: # is needed in make_predictions.py
        pickle.dump(reverse_mapping, file)
    encoded_setlist_string_list = apply_mapping_to_corpus(setlist_string_list)
    sequences_array = creating_sequences_for_model(encoded_setlist_string_list)
    with open(name + '_sequences_array', "wb") as file: # is needed in make_predictions.py
        pickle.dump(sequences_array, file)
    X_train, X_test, y_train, y_test = create_X_y(sequences_array)
    y_train_hot, y_test_hot, num_classes = one_hot_encode(unique_songs)
    model = train_model(num_classes)
    model.save(name + "_model") # # is needed in make_predictions.py
    print(Figlet().renderText('Finished!'))
    print("Let's look at the accuracy and the loss of our model:\n\n")
    evaluating_model(model)
