#!/usr/bin/env python3
"""
This module contains a function get_page that tracks the number of times a web
page is accessed
"""
import redis
import requests

count = 0


def get_page(url: str) -> str:
    """
    Track how many times a web page is accessed

    Args:
        url: The uniform resource locator to reach the website

    Return: count of how many time the web page is accessed in ten seconds
    """
    r = redis.Redis()
    resp = requests.get(url)
    r.incr(f"count:{url}")
    r.setex(f"cached:{url}", 10, r.get(f"cached:{url}"))
    return resp.text


if __name__ == "__main__":
    get_page('http://slowwly.robertomurray.co.uk')
