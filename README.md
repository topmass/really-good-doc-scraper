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

### Using UV (Recommended)

Install uv if you haven't already

    pip install uv

Create and activate virtual environment

    uv venv
    uv python install 3.12
    uv python pin 3.12

Install dependencies

    uv pip install -r requirements.txt
    uv run playwright install

### Using Traditional venv

    python -m venv .venv
    .venv/Scripts/activate # On Windows
    source .venv/bin/activate # On Unix/MacOS
    pip install -r requirements.txt
    playwright install

## Usage

Run the scraper by providing a starting URL:

### Using UV

    uv run ws.py https://example.com

### Using Python directly

    python ws.py https://example.com

## Output Structure

The scraper creates two main directories:

- `scraped_pages`: Contains markdown files for each scraped page.
- `url_list`: Contains CSV files for each domain, listing all processed URLs.

Each markdown file is named after the sanitized URL and saved in the corresponding domain folder.