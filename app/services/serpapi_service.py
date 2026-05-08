import requests

from app.config import SERPAPI_API_KEY



def search_book_content(query):

    url = "https://serpapi.com/search"

    params = {
        "engine": "google",
        "q": query,
        "api_key": SERPAPI_API_KEY,
        "num": 5
    }

    response = requests.get(url, params=params)

    data = response.json()
    search_results = []

    organic_results = data.get("organic_results", [])

    for result in organic_results:

        snippet = result.get("snippet")

        if snippet:
            search_results.append(snippet)

    return "".join(search_results)