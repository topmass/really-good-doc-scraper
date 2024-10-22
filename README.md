# Web Scraper with Crawlee

A simple but powerful web scraper that crawls websites and saves content in markdown format while maintaining document structure. The scraper automatically organizes content by domain and removes common boilerplate elements like headers and footers.

## Features

- Crawls websites respecting same-domain policy
- Saves content as clean markdown files
- Removes headers, footers, and navigation elements
- Maintains document structure (headings, paragraphs, lists)
- Organizes content by domain
- Tracks URLs in domain-specific CSV files

## Setup

### Using venv 
(you may try without venv if you want, recommended python version 3.12 or higher)

    python -m venv .venv
    .venv/Scripts/activate # On Windows
    source .venv/bin/activate # On Unix/MacOS
    pip install -r requirements.txt
    playwright install

## Usage

Run the scraper by providing a starting URL:

### Automatically Crawling Multiple Pages

    python ws.py https://example.com

### Specifying a list of urls (local csv file)

    python ws.py link_to_file.csv

## Output Structure

The scraper creates two main directories:

- `scraped_pages`: Contains markdown files for each scraped page.
- `url_list`: Contains CSV files for each domain, listing all processed URLs.

Each markdown file is named after the sanitized URL and saved in the corresponding domain folder.