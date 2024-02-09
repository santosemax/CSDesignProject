from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import googlesearch
import wikipediaapi

app = Flask(__name__)

# SQLite database setup (Articles will be used to host the retrieved articles)
conn = sqlite3.connect('articles.db')
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS articles (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, url TEXT)')
conn.commit()
conn.close()

# Function to perform web scraping from Google
def scrape_google_results(search_term):
    articles = []
    for result in googlesearch.search(search_term):
        title = result.split(' - ')[0]
        articles.append({'title': title, 'url': result})
    print(f'\n\nGOOGLE RESULTS:\n {articles}')
    return articles

# Function to perform web scraping from Wikipedia
def scrape_wikipedia_results(search_term):
    wiki_wiki = wikipediaapi.Wikipedia('MyProjectName', 'en')
    page_py = wiki_wiki.page(search_term)
    if page_py.exists():
        print(f'\n\nWIKIPEDIA RESULTS:\n {page_py.fullurl}')
        return [{'title': page_py.title, 'url': page_py.fullurl}]
    else:
        return []

# MAIN PAGE
@app.route('/')
def index():
    return render_template('index.html')

# SEARCH
@app.route('/search', methods=['POST'])
def search():
    search_term = request.form['search_term']

    # DO WEB SCRAPING HERE
    google_articles = scrape_google_results(search_term)
    wikipedia_articles = scrape_wikipedia_results(search_term)

    # Combine the results
    articles = google_articles + wikipedia_articles

    # Insert scraped data into the database
    conn = sqlite3.connect('articles.db')
    c = conn.cursor()
    for article in articles:
        c.execute('INSERT INTO articles (title, url) VALUES (?, ?)', (article['title'], article['url']))
    conn.commit()
    conn.close()

    return redirect(url_for('display_results', search_term=search_term))

# RETRIEVE
@app.route('/results/<search_term>')
def display_results(search_term):
    # Retrieve data from the database based on the search term (see index.html)
    conn = sqlite3.connect('articles.db')
    c = conn.cursor()
    c.execute('SELECT * FROM articles WHERE title LIKE ?', ('%' + search_term + '%',))
    results = c.fetchall()
    conn.close()

    return render_template('results.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
