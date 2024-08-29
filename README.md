# Agentic Scraper

web scraper designed to extract product information from commercial websites using AgentQL and Playwright and store the results in a CSV file.

## Features

- Scrapes product name, price, number of reviews, and rating from commercial websites
- Handles pagination to scrape multiple pages of results
- Stores scraped data in a CSV file

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.9+
- pip 

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/amazon-product-scraper.git
   cd agentic-webscraper
   ```

2. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

3. Install Playwright browsers:
   ```
   playwright install
   ```

4. Get your AgentQL API key from [AgentQL Dashboard](https://dev.agentql.com/api-keys)

5. Create a `.env` file in the project root and add your AgentQL API key:
   ```
   AGENTQL_API_KEY=your_api_key_here
   ```

## Usage

1. Open `agent.py` and modify the `url` variable if you want to scrape a different search results page.

2. Run the scraper:
   ```
   python agent.py
   ```


## Configuration

You can modify the following variables in `agent.py` to customize the scraper's behavior:

- `url`: The  search results URL to scrape
- `PRODUCT_QUERY`: The GraphQL query for product data
- `PAGINATION_QUERY`: The GraphQL query for pagination data


## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [AgentQL](https://dev.agentql.com/) for providing the querying capabilities
- [Playwright](https://playwright.dev/) for browser automation# Agentic-Scraper
