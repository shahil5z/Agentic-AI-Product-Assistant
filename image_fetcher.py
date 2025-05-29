import requests
from io import BytesIO
from PIL import Image
from serpapi import GoogleSearch
from dotenv import load_dotenv
import os

load_dotenv()
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

def fetch_product_image(product_name: str) -> Image.Image | None:
    if not SERPAPI_API_KEY:
        print("Error: SERPAPI_API_KEY not found in environment variables.")
        return None

    params = {
        "engine": "google",
        "q": product_name,
        "tbm": "isch",
        "api_key": SERPAPI_API_KEY,
        "num": 1
    }
    search = GoogleSearch(params)
    results = search.get_dict()

    try:
        image_url = results["images_results"][0]["original"]
        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content))
        return img
    except (KeyError, IndexError, requests.RequestException):
        return None
