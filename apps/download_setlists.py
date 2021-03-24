import re
import requests
import time
import pandas as pd
import pickle
from bs4 import BeautifulSoup
from pyfiglet import Figlet

headers =  {"User Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0"}
BASE_LINK = 'https://www.setlist.fm/search?page='


def input_artist():
    """Collect artist name"""
    name = "dummy"  # otherwise loop does not start
    name = input("\nPlease enter the name of the artist to scrape. Press 'Enter' to finish:\n\n ")
    name = name.lower().strip().replace(' ', '-').replace('+', '_')
    return name


def create_concert_links(name):
    """Generates the links to the concert pages to scrape from"""
    concert_links =[]
    for i in range(2,80):
        concert_links.append(BASE_LINK + str(i) + '&query=' + name)
    return concert_links


def download_concert_links(concert_links):
    '''
    Goes through the list to the concert pages, dowloads them and
    appends them to a single list
    '''
    print('\n\nScraping concert pages...\n\n')
    scraped_concert_links = []
    for link in concert_links:
        time.sleep(1.5)
        http_request = requests.get(link, headers=headers)
        scraped_concert_links.append(http_request.text)
    scraped_concert_links= ' '.join(scraped_concert_links)
    return scraped_concert_links


def get_setlist_urls(scraped_concert_links):
    '''
    extracts all urls to concert setlists from concert pages list created above
    with the help of a defined regex pattern
    '''
    print('Extracting urls to concert setlists...\n\n')
    pattern = '<a href=".*(setlist/.*' + name + '/.+html)'
    setlist_urls = re.findall(pattern, scraped_concert_links)
    return setlist_urls


def complete_urls(setlist_urls):
    """Completes the setlist urls adding http://setlist.fm/ to each url"""
    complete_setlist_urls = []
    for i in setlist_urls:
        link = "http://www.setlist.fm/" + i
        complete_setlist_urls.append(link)
    return complete_setlist_urls


def extract_setlist(complete_setlist_urls):
    '''
    * goes through the list of setlist urls,
    * finds the songs with the help of a pattern defined using BeautifulSoup
    * appends all extracted songs to a list, adding tour name and year
    '''
    print('Extracting setlists...\n\n')
    setlist_data = []
    for url in complete_setlist_urls:
        time.sleep(1)
        # opens the page
        http_request = requests.get(url, headers=headers)
        html_string = http_request.text
        # extracts songs, name of tour, and year of the concert
        soup = BeautifulSoup(html_string, features="lxml")
        song_label = soup.body.find_all(class_="songLabel")
        tour_name = url.split('/')[-1].split('.')[0]
        year = url.split('/')[-2]
        # appends songs without tags
        song_list = '| '.join([x.text for x in song_label])
        # removes commas from song titles
        song_list = song_list.replace(',','')
        song_list_new = song_list.replace('|',',')
        setlist_data.append([tour_name, year, song_list_new])
    return setlist_data


def create_dataframe(setlist_data):
    '''
    * creates a DataFrame out of the setlist data with columns 'venue',
      'concert_year', and 'setlist'
    * drops rows that contain less than 10 songs in setlist column
    * drops rows with NaNs
    * saves DataFrame with the name of the artist in location where file is executed
    '''
    print('Creating a DataFrame...\n\n')
    columns=['venue','concert_year','setlist']
    data = setlist_data
    df = pd.DataFrame(data,columns=columns)
    df["setlist"] = df["setlist"].loc[df['setlist'].str.count(',') >= 10]
    df = df.dropna()
    df.to_csv(name + '.csv')
    return df


if __name__ == '__main__':
    print(Figlet().renderText('Setlist Scraper\n'))
    name = input_artist()
    concert_links = create_concert_links(name)
    scraped_concert_links = download_concert_links(concert_links)
    setlist_urls = get_setlist_urls(scraped_concert_links)
    complete_setlist_urls = complete_urls(setlist_urls)
    setlist_data = extract_setlist(complete_setlist_urls)
    df = create_dataframe(setlist_data)
    print(Figlet().renderText('Finished!\n'))
    concert_count = df.shape[0]
    print(f'{concert_count} concert setlists have been scraped successfully!\n\n')
