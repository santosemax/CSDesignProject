# User Documentation (modified for final version of app)
- Was not sure if this is the same as the user interface specification. I saw it was optional and added just in case. It clarifies our UI and how to use it.

## Table of Contents
- [Overview](#overview)
- [Functions](#functions)
  - [Search](#search)
  - [Filter](#filter)
  - [Caching](#caching)
- [Results](#results)

## Overview
SUBMARINE is a more efficient way to search for specific information from web articles done on films, literature, and other forms of art. Instead of browsing for the piece of information you’re looking for, Submarine will pull what you’re looking for.

### Example Queries
- Jaws 2
- Abbey Road
- Fahrenheit 451

## Functions

### Search
To use the search function, press spacer or click on the spotlight icon, and then type in your query and hit enter. SUBMARINE will return the top results of your search. When looking for a specific piece of information, like an author, use the filter function.

### Filter
The filter function allows a user to click and choose which pieces of information they’re looking for:

- Author
- Producer
- Director
- Musician
- Artist

The filter function also allows for the specification of file types. Some of these include:

- Academic articles
- PDFs
- epubs/electronic books (from sites like Internet Archive)

### Caching
Each search, if not searched before, will be cached. This is the reason for blazing fast speed when searching certain queries.

## Results

### Main Results
Once the search has been initiated, on the right side of the page are Wikipedia results if they are relevant to the search query and on the left are related web pages and articles.

### Google Results
For now, these related web pages and articles are from Google. They use the googlesearch-python API ([Link](https://pypi.org/project/googlesearch-python/)). They will be specified to include only select file types such as pdfs and specific web sites. Within the above filter, they may even further specify the file types.

### Wikipedia Results
For the Wikipedia-related articles, the search engine will do its best to get the most relevant Wikipedia article. This is done using the wikipedia-api Python library ([Link](https://pypi.org/project/Wikipedia-API/)). It will display the main contents of the article: summary, image, and data at the top of the Wikipedia page; and, beneath this page are recommendations to other, relevant, Wikipedia pages just in case the search engine has not provided the correct page that the user was searching for.

### Articles
At the top of the page, articles will show after the first entry (which is the wikipedia result).

### Films
Below the articles section are films. You can navigate this by using the panel in the top left of the page. It includes the film cover, the IMDb link, and information on the film.

### Albums
This section (also navigable by the top left panel) brings you an album cover, year produced, and the artists who worked on the album. It is designed to bring you the five most likely albums for your query. These albums are connected to spotify.

### Books
The last section are results gathered from Google's open book database. The author, year published, and book cover are all shown here.
