# Setlist Predictor
## Project description
This Python application scrapes setlists from a chosen artists from setlist.fm, trains a neural network with word embedding and LSTM cells using Tensorflow and predicts a list of songs an artist could play at a concert.

## Python applications and how to use them
The project consists of the following 3 Python applications:

- **download_setlists.py**

This file scrapes setlists according to a defined number of pages (example of a page with links to concerts:https://www.setlist.fm/search?query=foo+fighters) from the website setlist.fm and saves them in a DataFrame consisting of a venue a year and a setlist column which is written to the disk using the name of the artist.

Information that needs to be entered in the file:
- User Agent for scraping (line 9)
- Define range in line 24 (number of pages to be scraped, for example 80)

![setlist_scraper](https://user-images.githubusercontent.com/72550661/109695076-cb839180-7b8b-11eb-9d8f-8589023f4f22.PNG)

Example showing scraping of Foo Fighters setlists


- **train_model.py**

The file named train_model.py finds the respective DataFrame upon entering the artist name, preprocesses the data and brings it into the required shape for model training. All setlists are appended to one string which is then split into sequences. The songs names are transformed into unique integers representing them. A Recurrent Neural Network with a Word Embedding and LSTM layer is trained, which learns by looking at the sequences of songs.

![model_trainer](https://user-images.githubusercontent.com/72550661/109695898-c1ae5e00-7b8c-11eb-86b2-cb39e1f6bdb4.PNG)

Screenshot of train_model.py


- **make predictions.py**

This python programme loads the respective model that has been saved during the execution of the train_model.py application and genereates a setlist with a defined length (default: 25 songs) and prints it in the console.



## Project example using Foo Fighters setlists

The model has been developed using Foo Fighters setlists.

Predicted Foo Fighters setlist:

The setlist ends with song no. 19. After that, the sequence is repeated from the beginning.

![setlist_prediction](https://user-images.githubusercontent.com/72550661/109697273-477ed900-7b8e-11eb-8137-18d9a13585ab.PNG)


Some plots that have been created based on the Foo Fighters corpus to visualize the performance of the model:

**Most frequently played Foo Fighters songs**

![most_frequent_songs](https://user-images.githubusercontent.com/72550661/110627944-d305f480-81a2-11eb-81cb-727215fa9f9c.PNG)



**Top 5 opening songs**

![openers_2](https://user-images.githubusercontent.com/72550661/110628012-e749f180-81a2-11eb-91a7-c9df8e8c13e0.PNG)





Most frequent position of some songs within a concert setlist:


**'The Pretender'**

![pretender](https://user-images.githubusercontent.com/72550661/110628308-25dfac00-81a3-11eb-85d4-115c749819ad.PNG)


**'Cheer Up Boys (Your Make Up Is Running)'**

![Cheer_up](https://user-images.githubusercontent.com/72550661/110628404-414ab700-81a3-11eb-9efe-078facd91869.PNG)


**'Best of You'**

![best_of_you](https://user-images.githubusercontent.com/72550661/110628444-4c054c00-81a3-11eb-9a20-c23588c0cdc6.PNG)





## Ideas for future improvements

- Give the model information about the age of the songs played (so far, the model understands which songs are played frequently but does not know whether a song is still likely to be played now)
- Incorporate data about the concert venue
