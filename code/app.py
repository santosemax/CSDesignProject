from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import googlesearch
import wikipediaapi
from imdb import IMDb

app = Flask(__name__)

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
        # print(f'\n\nGOOGLE RESULTS:\n {articles}')
    return articles

# Function to perform web scraping from Wikipedia
def scrape_wikipedia_results(search_term):
    wiki_wiki = wikipediaapi.Wikipedia('Submarine Search Engine', 'en')
    page_py = wiki_wiki.page(search_term)
    if page_py.exists():
        # Include source information in the dictionary
        print(f'\n\nWIKIPEDIA RESULTS:\n {page_py.fullurl}')
        return [{'title': page_py.title, 'url': page_py.fullurl, 'search_phrase': search_term, 'source': 'Wikipedia'}]
    else:
        return []

# Function to search for film using IMDbPY
def search_film(search_term):
    ia = IMDb()
    search_results = ia.search_movie(search_term)
    if search_results:
        # Return the first search result
        movie_id = search_results[0].movieID
        movie = ia.get_movie(movie_id)
        return movie
    else:
        return None

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
        
        # Search for film
        film = search_film(search_term)
        if film:
            # Extract relevant information from the movie object
            title = film.get('title', 'N/A')
            imdb_url = f"https://www.imdb.com/title/tt{film.movieID}/"
            summary = film.get('plot outline', 'N/A')
            cast = ', '.join(actor['name'] for actor in film.get('cast', []))
            director = ', '.join(director['name'] for director in film.get('director', []))
            img_url = film.get('full-size cover url', 'N/A')
            
            # Save film information into the database
            c.execute('INSERT INTO articles (title, url, search_phrase, source) VALUES (?, ?, ?, ?)',
                      (title, imdb_url, search_term, 'IMDb'))
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
