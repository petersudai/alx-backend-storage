#!/usr/bin/env python3
"""
Main file to test the web cache and access tracker.
"""
from web import get_page


if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk/delay/5000/url/http://www.example.com"
    
    # Fetch the URL content and print it
    content = get_page(url)
    print(content)
    
    # Print the access count for the URL
    count = redis_client.get(f"count:{url}")
    print(f"Access count for {url}: {count.decode('utf-8')}")
