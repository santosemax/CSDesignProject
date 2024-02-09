from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from scrape import Scraper

app = Flask(__name__)

# SQLite database setup (Articles will be used to host the retrieved articles)
conn = sqlite3.connect('articles.db')
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS articles (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, url TEXT)')
conn.commit()
conn.close()

# MAIN PAGE
@app.route('/')
def index():
    return render_template('index.html')

# SEARCH
@app.route('/search', methods=['POST'])
def search():
    search_term = request.form['search_term']

    scraper = Scraper(False)
    title, url = scraper.scrape(search_term)
    


    # Store data as collection of articles
    articles = [
        {'title': title, 'url': url}
    ]

    # Insert data into the database
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
