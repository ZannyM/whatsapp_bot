import requests
from dotenv import load_dotenv
import os

def get_quote(category):
    load_dotenv()
    api_url = 'https://api.api-ninjas.com/v1/quotes?category={}'.format(category)
    response = requests.get(api_url, headers={'X-Api-Key': os.environ.get('API_KEY')})
    if response.status_code == requests.codes.ok:
        if response.json() == []:
            # return f"available quotes: {category()}"
            return "category not found "
        else:
            quote = response.json()
            return quote

    else:
        print("Error:", response.status_code, response.text)


if __name__ == "__main__":
    print(get_quote("art"))