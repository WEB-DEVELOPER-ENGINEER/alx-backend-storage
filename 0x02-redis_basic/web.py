#!/usr/bin/env python3
"""Implementing an expiring web cache and request counter"""
from functools import wraps
import redis
import requests
from typing import Callable

# Create a Redis connection
redis_ = redis.Redis()

# Constants
CACHE_EXPIRATION_SECONDS = 600  # Set the cache expiration time to 10 minutes

def count_requests(method: Callable) -> Callable:
    """Decorator for counting requests"""
    @wraps(method)
    def wrapper(url):
        """Wrapper for the decorator"""
        redis_.incr(f"count:{url}")
        cached_html = redis_.get(f"cached:{url}")
        if cached_html:
            return cached_html.decode('utf-8')
        try:
            html = method(url)
            redis_.setex(f"cached:{url}", CACHE_EXPIRATION_SECONDS, html)
            return html
        except requests.RequestException as e:
            # Handle request exceptions (e.g., network issues or invalid URLs)
            print(f"Error while fetching {url}: {e}")
            return ""

    return wrapper

@count_requests
def get_page(url: str) -> str:
    """Get the HTML content of a URL with the requests module and return it"""
    req = requests.get(url)
    req.raise_for_status()  # Raise an exception for HTTP errors (4xx and 5xx)
    return req.text

if __name__ == "__main__":
    # Example usage
    url = "https://example.com"
    html = get_page(url)
    if html:
        print(f"Content of {url}:\n{html}")

