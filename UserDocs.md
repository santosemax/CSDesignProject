# User Documentation

[Application Name] is a more efficient way to search for specific information from web articles done on films, literature, and other forms of art. Instead of browsing for the piece of information you’re looking for, [Application] will pull what you’re looking for.

## Table of Contents
- [Overview](#overview)
- [Functions](#functions)
  - [Search](#search)
  - [Filter](#filter)
  - [Caching](#caching)
- [Results](#results)

## Overview
[Application Name] is a more efficient way to search for specific information from web articles done on films, literature, and other forms of art. Instead of browsing for the piece of information you’re looking for, [Application] will pull what you’re looking for.

### Example Queries
- Jaws 2 director
- Abbey Road producers
- Fahrenheit 451 author

## Functions

### Search
To use the search function, type in your query and hit “search”. [Application] will return the top results of your search. When looking for a specific piece of information, like an author, use the filter function.

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
If you wish to save the data you searched for, use the cache function after the results are returned. Cached info can be returned to later.

## Results

### Main Results
Once the search has been initiated, on the right side of the page are Wikipedia results if they are relevant to the search query and on the left are related web pages and articles.

### Google Results
For now, these related web pages and articles are from Google. They use the googlesearch-python API ([Link](https://pypi.org/project/googlesearch-python/)). They will be specified to include only select file types such as pdfs and specific web sites. Within the above filter, they may even further specify the file types.

### Wikipedia Results
For the Wikipedia-related articles, the search engine will do its best to get the most relevant Wikipedia article. This is done using the wikipedia-api Python library ([Link](https://pypi.org/project/Wikipedia-API/)). It will display the main contents of the article: summary, image, and data at the top of the Wikipedia page; and, beneath this page are recommendations to other, relevant, Wikipedia pages just in case the search engine has not provided the correct page that the user was searching for.
