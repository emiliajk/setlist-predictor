# Setlist Predictor
## Project description
This Python application scrapes setlists from a chosen artists from setlist.fm, trains a neural network using Tensorflow and predicts a list of songs an artist could play at a concert.

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

The file named train_model.py finds the respective DataFrame upon entering the artist name, preprocesses the data and brings it into the required shape for model training. All setlists are appended to one string which is then split into sequences. The songs names are transformed into unique integers representing them. A Recurrent Neural Network with a Word Embedding and LSTM layer is trained.

![model_trainer](https://user-images.githubusercontent.com/72550661/109695898-c1ae5e00-7b8c-11eb-86b2-cb39e1f6bdb4.PNG)

Screenshot of train_model.py
