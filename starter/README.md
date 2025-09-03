# Scrapy Starter Project

This directory contains a minimal Scrapy project configured with best practices
and managed using the [uv](https://github.com/astral-sh/uv) package manager.

## Setup

Create a virtual environment and install dependencies:

```bash
uv sync
```

## Running the spider

```bash
uv run scrapy crawl scrapy_docs
```

The spider crawls the Scrapy documentation, converts each page to Markdown and
writes the files under `out/md/{lang}/{version}/`.
