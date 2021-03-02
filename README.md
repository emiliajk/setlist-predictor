# Setlist Predictor
## Project description
This Python application scrapes setlists from a chosen artists from setlist.fm, trains a neural network using Tensorflow and predicts a list of songs an artist could play at a concert.

## Python applications and how to use them
The project consists of the following 3 Python applications:

- **download_setlists.py**
This file scrapes setlists according to a defined number of pages (example of a page with links to concerts:https://www.setlist.fm/search?query=foo+fighters) and saves them in a DataFrame consisting of a venue a year and a setlist column which is written to the disk using the name of the artist.


