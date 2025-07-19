import requests
from bs4 import BeautifulSoup, Comment

def scrape_body(url: str, return_html: bool = False) -> str:
    """
    Fetches the given URL and extracts its <body> content, cleaned of scripts,
    styles, navigation, header/footer, comments, and other non-essential tags.

    Args:
        url (str): The URL to scrape.
        return_html (bool): If True, returns the cleaned HTML of the <body>;
                            otherwise, returns plain text.

    Returns:
        str: Cleaned HTML or text content of the <body>.
    """
    # Fetch the page
    response = requests.get(url)
    response.raise_for_status()

    # Parse HTML
    soup = BeautifulSoup(response.content, 'html.parser')

    # Remove unwanted tags
    for tag_name in ['script', 'style', 'header', 'footer', 'nav', 'aside', 'form', 'noscript', 'details']:
        for tag in soup.find_all(tag_name):
            tag.decompose()

    # Remove HTML comments
    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        comment.extract()

    # Extract body
    body = soup.body
    if body is None:
        return ''

    if return_html:
        # Return cleaned HTML of the body
        # Strip attributes from tags to keep only content structure
        for tag in body.find_all(True):
            tag.attrs = {}
        return str(body)
    else:
        # Get plain text, preserving line breaks
        text = body.get_text(separator='\n', strip=True)
        # Optionally, collapse multiple blank lines
        lines = [line for line in text.splitlines() if line.strip()]
        return '\n'.join(lines)

def get_title(web_url: str) -> str:
    """
    Fetches the title of a web page.

    Args:
        web_url (str): The URL of the page

    Returns:
        str: The title of the page
    """
    # Fetch the page
    response = requests.get(web_url)
    response.raise_for_status()

    # Parse HTML
    soup = BeautifulSoup(response.content, 'html.parser')
    link = soup.find_all(name="title")[0]
    return link.text