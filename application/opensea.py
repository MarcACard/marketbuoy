import requests

BASE = "https://api.opensea.io/api/v1"


def get_collection(collection_slug: str):
    """Retrieve Collection Info from OpenSea.io API"""
    url = f"{BASE}/collection/{collection_slug}"

    resp = requests.get(url)

    return resp.json()["collection"]


def get_collection_stats(collection_slug: str):
    """Retrieve Collection Stats from OpenSea.io API"""
    url = f"{BASE}/collection/{collection_slug}/stats"

    resp = requests.get(url)

    return resp.json()
