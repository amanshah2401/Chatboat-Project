import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class WebCrawler:
    """
    A simple web crawler to extract text content from a website.
    """
    def __init__(self, base_url, max_pages=10):
        self.base_url = base_url
        self.max_pages = max_pages
        self.visited_urls = set()
        self.pages_content = []

    def is_valid_url(self, url):
        """
        Check if the URL belongs to the same domain as the base URL.
        """
        parsed_base = urlparse(self.base_url)
        parsed_url = urlparse(url)
        return parsed_url.netloc == parsed_base.netloc or not parsed_url.netloc

    def clean_text(self, soup):
        """
        Remove scripts, styles, and extract text from HTML.
        """
        for script_or_style in soup(["script", "style", "header", "footer", "nav"]):
            script_or_style.decompose()
        
        # Get text and handle whitespace
        lines = (line.strip() for line in soup.get_text().splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        return text

    def crawl(self, url=None):
        """
        Recursive crawl function.
        """
        if url is None:
            url = self.base_url

        if url in self.visited_urls or len(self.visited_urls) >= self.max_pages:
            return

        logger.info(f"Crawling: {url}")
        self.visited_urls.add(url)

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'lxml')
            
            cleaned_text = self.clean_text(soup)
            self.pages_content.append({
                "url": url,
                "content": cleaned_text
            })

            # Find and follow links
            for link in soup.find_all('a', href=True):
                new_url = urljoin(url, link['href'])
                # Remove fragments
                new_url = new_url.split('#')[0]
                if self.is_valid_url(new_url):
                    self.crawl(new_url)

        except Exception as e:
            logger.error(f"Failed to crawl {url}: {e}")

    def get_all_content(self):
        """
        Return the list of extracted content.
        """
        return self.pages_content

if __name__ == "__main__":
    crawler = WebCrawler("https://docs.python.org/3/tutorial/index.html", max_pages=3)
    crawler.crawl()
    for page in crawler.get_all_content():
        print(f"URL: {page['url']}\nContent Preview: {page['content'][:200]}...\n")
