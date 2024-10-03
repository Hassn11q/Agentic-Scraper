import streamlit as st
from streamlit_tags import st_tags_sidebar
import pandas as pd
import json
from datetime import datetime
import os
from dotenv import load_dotenv
import agentql
from agentql.sync_api import ScrollDirection
import time
from io import StringIO
from pydantic import BaseModel

# Load environment variables
load_dotenv()

def serialize_pydantic(obj):
    if isinstance(obj, BaseModel):
        return obj.dict()
    raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')

# Initialize Streamlit app
st.set_page_config(page_title="Agentic Scraper", page_icon="🕷️")
st.title("Agentic Scraper 🕷️")

# Initialize session state variables
if 'results' not in st.session_state:
    st.session_state['results'] = None
if 'perform_scrape' not in st.session_state:
    st.session_state['perform_scrape'] = False

# Sidebar components
st.sidebar.title("Scraper Settings")
url_input = st.sidebar.text_input("Enter URL")

# Field selection
show_fields = st.sidebar.toggle("Enable Field Selection")
selected_fields = []
if show_fields:
    selected_fields = st_tags_sidebar(
        label='Select fields to extract:',
        text='Press enter to add a field',
        value=[],
        suggestions=[],
        maxtags=-1,
        key='fields_input'
    )

st.sidebar.markdown("---")

# Pagination settings
use_pagination = st.sidebar.toggle("Enable Pagination")
num_pages = 1
if use_pagination:
    num_pages = st.sidebar.number_input("Number of pages to scrape:", min_value=1, value=1)

st.sidebar.markdown("---")

def start_scraping_session(url):
    """Initialize and return an AgentQL session"""
    session = agentql.start_session(url)
    session.driver.scroll_to_bottom()
    return session

def scrape_items(session, fields, num_pages):
    """Scrape elements from url"""
    all_products = []
    
    # Construct the GraphQL query based on user-selected fields
    items_query = "{"  
    items_query += "results { products[] {" 
    for field in fields:
        items_query += f"{field} " 
    items_query += "} } }" 

    pagination_query = """
    {
        next_page_button_enabled
        next_page_button_disabled
    }
    """

    for page in range(1, num_pages + 1):
        st.write(f"Scraping page {page}")
        
        # Fetch items data
        elements = session.query(items_query) 
        items_data = elements.to_data()['results']['products'] 
        all_products.extend(items_data)  # Extend the list with new products
        st.write(f"Scraped {len(items_data)} products successfully")
        
        # Check pagination status
        pagination = session.query(pagination_query)
        pagination_data = pagination.to_data()
        if not pagination_data['next_page_button_enabled'] or pagination_data['next_page_button_disabled']:
            st.write("Reached the last page. Scraping complete.")
            break
        
        # Navigate to the next page
        pagination.next_page_button_enabled.click()
        st.write("Navigated to the next page")
        session.driver.scroll_to_bottom()
        time.sleep(2)  # Wait for the page to load
    
    return all_products

def perform_scrape():
    try:
        session = start_scraping_session(url_input)
        products = scrape_items(session, selected_fields, num_pages)
        return products
    except Exception as e:
        st.error(f"An error occurred during scraping: {str(e)}")
        st.write("Debug information:")
        st.write(f"URL: {url_input}")
        st.write(f"Selected fields: {selected_fields}")
        st.write(f"Number of pages: {num_pages}")
        return None
    finally:
        if 'session' in locals():
            session.stop()

if st.sidebar.button("Scrape"):
    with st.spinner('Please wait... Data is being scraped.'):
        products = perform_scrape()
        st.session_state['results'] = products
        st.session_state['perform_scrape'] = True

# Display results if they exist in session state
if st.session_state['results']:
    products = st.session_state['results']
    
    # Display scraping details in sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Scraping Details")
    st.sidebar.markdown(f"**Total Products Scraped:** {len(products)}")

    # Display scraped data in main area
    st.subheader("Scraped Data")
    df = pd.DataFrame(products)
    st.dataframe(df)

    # Download buttons
    st.markdown("### Download Options")
    
    # CSV download
    csv = df.to_csv(index=False)
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="scraped_products.csv",
        mime="text/csv",
    )
    
    # JSON download
    json_str = df.to_json(orient="records")
    st.download_button(
        label="Download JSON",
        data=json_str,
        file_name="scraped_products.json",
        mime="application/json",
    )

    # Clear results button
    if st.button("Clear Results"):
        st.session_state['results'] = None
        st.session_state['perform_scrape'] = False
        st.experimental_rerun()

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit and AgentQL")

if __name__ == "__main__":
    pass  # The Streamlit app is already running at this point
















