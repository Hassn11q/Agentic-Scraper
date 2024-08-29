# Import required libraries
from dotenv import load_dotenv
import agentql
from agentql.sync_api import ScrollDirection
import csv
import time

# Load environment variables
load_dotenv()

# GraphQL query to fetch product details
PRODUCT_QUERY = """
{
    results {
        products[] {
            product_name
            product_price
            num_reviews
            rating
        }
    }
}
"""

# GraphQL query to check pagination status
PAGINATION_QUERY = """
{
    next_page_button_enabled
    next_page_button_disabled
}
"""

def start_scraping_session(url):
    """Initialize and return an AgentQL session"""
    session = agentql.start_session(url)
    session.driver.scroll_to_bottom()
    return session

def write_product_to_csv(writer, product):
    """Write a single product to the CSV file"""
    writer.writerow(product)
    print(f"Product written to CSV: {product['product_name']}")

def main():
    # URL for Amazon search results
    url = "https://www.amazon.sa/s?k=macbook+pro+m3&crid=3OVD0YRB3FI6A&sprefix=macbook+pro+%2Caps%2C410&ref=nb_sb_ss_pltr-xclick_1_12"
    
    # Start the scraping session
    session = start_scraping_session(url)

    try:
        with open("Products.csv", "w", newline="", encoding="utf-8") as file:
            columns = ["product_name", "product_price", "num_reviews", "rating"]
            writer = csv.DictWriter(file, fieldnames=columns)
            writer.writeheader()

            page_number = 1
            while True:
                print(f"\nScraping page {page_number}")

                # Fetch product data
                products = session.query(PRODUCT_QUERY)
                product_data = products.to_data()['results']['products']
                print(f"Scraped {len(product_data)} products successfully")

                # Write products to CSV
                for product in product_data:
                    write_product_to_csv(writer, product)

                # Check pagination status
                pagination = session.query(PAGINATION_QUERY)
                pagination_data = pagination.to_data()

                if not pagination_data['next_page_button_enabled'] or pagination_data['next_page_button_disabled']:
                    print("Reached the last page. Scraping complete.")
                    break

                # Navigate to the next page
                pagination.next_page_button_enabled.click()
                print("Navigated to the next page")
                session.driver.scroll_to_bottom()
                time.sleep(2)  # Wait for the page to load

                page_number += 1

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        session.stop()
        print("Scraping session ended")

if __name__ == "__main__":
    main()