from .api_call import make_api_call

def get_quote() -> dict:
    url = "https://zenquotes.io/api/today"
    try:
        response = make_api_call(url)
        if response and isinstance(response, list) and len(response) > 0:
            quote_data = response[0]
            return {
                "quote": quote_data.get("q", "No quote available."),
                "author": quote_data.get("a", "Unknown")
            }
        else:
            return {"quote": "No quote available.", "author": "Unknown"}
    except Exception as e:
        return {"quote": "Error fetching quote.", "author": str(e)}


if __name__ == "__main__":
    quote = get_quote()
    print(f"Quote: {quote['quote']}\nAuthor: {quote['author']}")