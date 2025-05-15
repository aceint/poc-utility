# 📰 Web Article Scraper API

## Overview

The **Web Article Scraper API** is a FastAPI-based web application that allows users to extract structured information from online articles. This API accepts a URL, scrapes the article, and returns key metadata such as the article's title, authors, publish date, text content, summary, keywords, and more. It uses the popular Python library **newspaper3k** to handle the scraping, and provides an easy-to-use API interface for developers to interact with.

This project serves as a backend scraper service and is ideal for applications that need to automatically retrieve and analyze articles, such as content aggregators, news websites, or research tools.

---

## Features

- **URL Input:** Accepts a URL to a news article, which is processed to extract various components of the article.
- **Content Extraction:**
  - Article Title
  - Authors
  - Publish Date
  - Top Image (if available)
  - Article Summary (via Natural Language Processing)
  - Keywords (via NLP for extracting important terms)
  - Full Article Text
- **File Storage:** The scraped data is saved in a `scraped_data.json` file for later reference.
- **API Response:** The extracted data is returned as a structured JSON response.
- **Interactive API Documentation:** Provides a Swagger UI interface (`/docs`) to test API functionality and interact with endpoints directly.

---

## Tech Stack

This project is built using the following technologies:

- **Python 3.7+**: Programming language used for developing the web scraper and API.
- **FastAPI**: Fast, modern web framework for building APIs with Python.
- **newspaper3k**: A Python library to extract article content, authors, and metadata from web pages.
- **Pydantic**: Used for data validation and serialization of request and response models.
- **Uvicorn**: A lightning-fast ASGI server for running FastAPI applications.
- **JSON**: The format used to save the scraped data in a local file.

---

## Installation

Follow these steps to set up and run the project on your local machine.

### 1. Clone the Repository

Begin by cloning the repository to your local system:

```bash
git clone https://github.com/your-username/web-article-scraper.git
cd web-article-scraper

