from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import googlesearch
import wikipediaapi
from imdb import IMDb
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests
import re

app = Flask(__name__)

# Initialize Spotify client
spotify_client_credentials_manager = SpotifyClientCredentials(client_id='d98da9dfe2ed4a7594ce4449653c066f',
                                                              client_secret='cf3fdc78a60142ec9ebb0050975005d2')
spotify = spotipy.Spotify(client_credentials_manager=spotify_client_credentials_manager)

# SQLite database setup (Articles will be used to host the retrieved articles)
def initialize_database():
    conn = sqlite3.connect('articles.db')
    c = conn.cursor()
    # Ensure the table includes a column for search terms and the source of the article
    c.execute('''
    CREATE TABLE IF NOT EXISTS articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        url TEXT,
        search_phrase TEXT,
        source TEXT  -- New column to indicate the source of the article
    )
    ''')
    conn.commit()
    conn.close()

initialize_database()

# Function to perform web scraping from Google
def scrape_google_results(search_term):
    articles = []
    for result in googlesearch.search(search_term):
        title = result.split(' - ')[0]
        # Include source information in the dictionary
        articles.append({'title': title, 'url': result, 'search_phrase': search_term, 'source': 'Google'})
    return articles

# Function to perform web scraping from Wikipedia
def scrape_wikipedia_results(search_term):
    wiki_wiki = wikipediaapi.Wikipedia('Submarine Search Engine', 'en')
    page_py = wiki_wiki.page(search_term)
    if page_py.exists():
        # Include source information in the dictionary
        return [{'title': page_py.title, 'url': page_py.fullurl, 'search_phrase': search_term, 'source': 'Wikipedia'}]
    else:
        return []

# Function to search for films using IMDbPY
def search_films(search_term):
    ia = IMDb()
    search_results = ia.search_movie(search_term)
    films = []
    for result in search_results[:5]:  # Limit to 5 results
        movie_id = result.movieID
        movie = ia.get_movie(movie_id)
        films.append(movie)
    return films

# Function to search for albums using Spotify
def search_albums(search_term):
    results = spotify.search(q=search_term, type='album', limit=5)
    albums = []
    for album in results['albums']['items']:
        album_title = album['name']
        albums.append((album_title, album))
    return albums

# Function to search for books using Google Books API
def search_books(search_term):
    url = f"https://www.googleapis.com/books/v1/volumes?q={search_term}&maxResults=5"  # Limit to 5 results
    response = requests.get(url)
    books = []
    if response.status_code == 200:
        data = response.json()
        if 'items' in data:
            for item in data['items']:
                book = item['volumeInfo']
                books.append(book)
    return books

# MAIN PAGE
@app.route('/')
def index():
    return render_template('index.html')

# SEARCH
@app.route('/search', methods=['POST'])
def search():
    search_term = request.form['search_term'].strip()

    # Check database for the search term
    conn = sqlite3.connect('articles.db')
    c = conn.cursor()
    c.execute('SELECT * FROM articles WHERE search_phrase = ?', (search_term,))
    existing_articles = c.fetchall()

    if not existing_articles:  # If this search term hasn't been used, scrape and save results
        wikipedia_articles = scrape_wikipedia_results(search_term)
        google_articles = scrape_google_results(search_term)
        
        articles = wikipedia_articles + google_articles

        for article in articles:
            # Adjust the SQL insert command to include the 'source' column
            c.execute('INSERT INTO articles (title, url, search_phrase, source) VALUES (?, ?, ?, ?)',
                      (article['title'], article['url'], search_term, article['source']))
        
        # Search for films
        films = search_films(search_term)
        for film in films:
            # Extract relevant information from the movie object
            title = film.get('title', 'N/A')
            imdb_url = f"https://www.imdb.com/title/tt{film.movieID}/"
            summary = film.get('plot outline', 'N/A')
            cast = ', '.join(actor['name'] for actor in film.get('cast', []))
            director = ', '.join(director['name'] for director in film.get('director', []))
            img_url = film.get('full-size cover url', 'N/A')
            
            # Save film information into the database
            c.execute('INSERT INTO articles (title, url, search_phrase, source) VALUES (?, ?, ?, ?)',
                      (('Title: ' + title), ('URL: ' + imdb_url), search_term, 'IMDb'))
            conn.commit()
            
            # Save additional information into the database
            c.execute('INSERT INTO articles (title, url, search_phrase, source) VALUES (?, ?, ?, ?)',
                      (f'Director: {director}', '', search_term, 'IMDb'))
            c.execute('INSERT INTO articles (title, url, search_phrase, source) VALUES (?, ?, ?, ?)',
                      (f'Cast: {cast}', '', search_term, 'IMDb'))
            c.execute('INSERT INTO articles (title, url, search_phrase, source) VALUES (?, ?, ?, ?)',
                      (f'Summary: {summary}', '', search_term, 'IMDb'))
            c.execute('INSERT INTO articles (title, url, search_phrase, source) VALUES (?, ?, ?, ?)',
                      (f'Image URL: {img_url}', '', search_term, 'IMDb'))
            conn.commit()
        
        # Search for albums
        albums = search_albums(search_term)
        for album_title, album in albums:
            # Extract relevant information from the album object
            artist = ', '.join(artist['name'] for artist in album['artists'])
            album_cover = album['images'][0]['url'] if album['images'] else 'N/A'
            release_date = album['release_date']
            total_tracks = album['total_tracks']
            
            # Save album information into the database
            c.execute('INSERT INTO articles (title, url, search_phrase, source) VALUES (?, ?, ?, ?)',
                      (f'Album Title: {album_title}', '', search_term, 'Spotify'))  # Include the album title
            c.execute('INSERT INTO articles (title, url, search_phrase, source) VALUES (?, ?, ?, ?)',
                      (f'Artist: {artist}', '', search_term, 'Spotify'))
            c.execute('INSERT INTO articles (title, url, search_phrase, source) VALUES (?, ?, ?, ?)',
                      (f'Album Cover: {album_cover}', '', search_term, 'Spotify'))
            c.execute('INSERT INTO articles (title, url, search_phrase, source) VALUES (?, ?, ?, ?)',
                      (f'Release Date: {release_date}', '', search_term, 'Spotify'))
            c.execute('INSERT INTO articles (title, url, search_phrase, source) VALUES (?, ?, ?, ?)',
                      (f'Total Tracks: {total_tracks}', '', search_term, 'Spotify'))
            conn.commit()
        
        # Search for books
        books = search_books(search_term)
        for book_info in books:
            # Extract relevant information from the book info
            title = book_info.get('title', 'N/A')
            author = ', '.join(book_info.get('authors', ['Unknown']))
            year = book_info.get('publishedDate', 'N/A')
            book_cover = book_info.get('imageLinks', {}).get('thumbnail', 'N/A')
            
            # Save book information into the database
            c.execute('INSERT INTO articles (title, url, search_phrase, source) VALUES (?, ?, ?, ?)',
                      (f'Book Title: {title}', '', search_term, 'Google Books'))  # Include the book title
            c.execute('INSERT INTO articles (title, url, search_phrase, source) VALUES (?, ?, ?, ?)',
                      (f'Author: {author}', '', search_term, 'Google Books'))
            c.execute('INSERT INTO articles (title, url, search_phrase, source) VALUES (?, ?, ?, ?)',
                      (f'Year of Publication: {year}', '', search_term, 'Google Books'))
            c.execute('INSERT INTO articles (title, url, search_phrase, source) VALUES (?, ?, ?, ?)',
                      (f'Book Cover: {book_cover}', '', search_term, 'Google Books'))
            conn.commit()
        
    conn.close()

    return redirect(url_for('display_results', search_term=search_term))

# RETRIEVE
@app.route('/results/<search_term>')
def display_results(search_term):
    search_term = search_term.strip()
    conn = sqlite3.connect('articles.db')
    c = conn.cursor()
    c.execute('SELECT * FROM articles WHERE search_phrase = ?', (search_term,))
    results = c.fetchall()
    conn.close()

    return render_template('results.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
