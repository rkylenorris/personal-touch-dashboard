import requests

def make_api_call(api_url: str) -> dict:
    """
    Makes an API call to the specified URL and returns the JSON response.

    Args:
        api_url (str): The URL of the API endpoint.

    Returns:
        dict: The JSON response from the API.
    """
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching data: {response.status_code} - {response.text}")
