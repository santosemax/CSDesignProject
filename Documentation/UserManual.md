# SUBMARINE User Manual

## Table of Contents
1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Functions](#functions)
   - [Search](#search)
   - [Filter](#filter)
   - [Caching](#caching)
4. [Results](#results)
   - [Main Results](#main-results)
   - [Google Results](#google-results)
   - [Wikipedia Results](#wikipedia-results)
   - [Articles](#articles)
   - [Films](#films)
   - [Albums](#albums)
   - [Books](#books)

## Introduction
Welcome to SUBMARINE! SUBMARINE is an efficient tool designed to help you quickly find specific information from web articles related to films, literature, and other forms of art. Instead of manually searching through articles, SUBMARINE extracts the information you need, saving you time and effort.

## Getting Started
To begin using SUBMARINE, simply follow these steps:

- Access SUBMARINE through your preferred web browser.
- Upon accessing the app, you'll be presented with a search interface.
- Enter your query into the search bar and hit enter.
- SUBMARINE will quickly generate results based on your query, allowing you to access relevant information with ease.

## Functions

### Search
The search function enables you to find specific information by entering your query into the search bar. SUBMARINE will return the top results related to your query. To initiate a search, simply type your query and press enter.

### Filter
The filter function allows you to refine your search results by selecting specific categories of information. You can filter by:
- Author
- Producer
- Director
- Musician
- Artist

Additionally, you can specify file types such as:
- Academic articles
- PDFs
- epubs/electronic books (from sites like Internet Archive)

### Caching
SUBMARINE caches each search, optimizing speed for subsequent searches. This ensures blazing-fast performance when searching for similar queries in the future.

## Results

### Main Results
Once you initiate a search, SUBMARINE displays relevant information on the right side of the page, including Wikipedia results if applicable, and related web pages and articles on the left.

### Google Results
Related web pages and articles are sourced from Google. These results are filtered to include select file types such as PDFs and specific websites, based on your preferences.

### Wikipedia Results
SUBMARINE utilizes the Wikipedia-API Python library to fetch the most relevant Wikipedia article related to your search query. The article summary, image, and top data are displayed, along with recommendations to other relevant Wikipedia pages.

### Articles
Displayed after the Wikipedia result, this section presents related articles gathered from the web.

### Films
Below the articles section, you'll find information on films related to your query. Navigate this section using the panel in the top left of the page. Each entry includes the film cover, IMDb link, and additional film details.

### Albums
Similarly, the albums section, also navigable by the top left panel, showcases album covers, year produced, and artist information. The top five albums related to your query are displayed, with links to Spotify for further exploration.

### Books
Finally, results from Google's open book database are displayed, featuring book covers, author names, and publication years.

With SUBMARINE, you can efficiently access the information you need from web articles, films, albums, and books, all in one convenient platform. Happy searching!
