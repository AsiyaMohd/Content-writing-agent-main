from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.tools import tool
import os
from dotenv import load_dotenv
import requests # New import
from bs4 import BeautifulSoup # New import
import re # New import
from urllib.parse import urlparse # New import
load_dotenv()
import re
from langchain_core.messages import ToolMessage

os.environ["TAVILY_API_KEY"]=os.getenv("TAVILY_API_KEY")

def is_url(text):
    """Checks if the input string is a valid URL."""
    try:
        result = urlparse(text)
        # Check for both scheme (http/https) and network location (domain)
        return all([result.scheme in ('http', 'https'), result.netloc])
    except:
        return False

def scrape_single_url(url):
    """Fetches and scrapes content from a single URL."""
    try:
        print(f"--- Scraping content from: url ---")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() 
        soup = BeautifulSoup(response.text, 'html.parser')

        # Target main content tags for text extraction
        text_content = ' '.join(p.text for p in soup.find_all(['p', 'h1', 'h2', 'h3', 'li']))
        
        # Clean up text
        clean_text = re.sub(r'\s+', ' ', text_content).strip()

        if not clean_text:
             return f"Scraping result from url: Successfully connected, but no significant text content was extracted."

        # Return the scraped content with a clear identifier
        print("------------------cleaned text---------------")
        print(clean_text)
        return f"Scraped Content from url :\n{clean_text}"
    
    except requests.RequestException as e:
        return f"Error scraping URL url: {e}. Falling back to search or returning an error."
    except Exception as e:
        return f"An unexpected error occurred during scraping: {e}"

url_pattern = re.compile(r'https?://[^\s]+')

def extract_urls_from_tool_messages(state):
    urls = []

    # state is like {"messages": [HumanMessage, ToolMessage, AIMessage, ...]}
    for msg in state.get("messages", []):
        if isinstance(msg, ToolMessage):
            # msg.content is a plain string
            found_urls = url_pattern.findall(msg.content)
            urls.extend(found_urls)
    
    return urls


@tool
def search_content(subject):
    """Search the web for relevant content using Tavily search or scrape a specific URL if the subject is a single URL."""
    print("--------------------------------tool triggered")

    # If the subject is a URL, perform direct scraping
    if is_url(subject):
        return scrape_single_url(subject)
    else:
        # Otherwise, perform a regular Tavily search
        s_tool=TavilySearchResults(max_results=25)
        res=s_tool.invoke(subject)
        return res
    
