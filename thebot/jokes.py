import requests
import os
from dotenv import load_dotenv

import requests

def get_joke(limit):
    load_dotenv()
    api_url = 'https://api.api-ninjas.com/v1/jokes?limit={}'.format(limit)
    response = requests.get(api_url, headers={'X-Api-Key': os.environ.get('API_KEY')})
    if response.status_code == requests.codes.ok:
        if response.json() == []:
            return "Joke Not Found"
        else:
            joke = response.json()
            return joke
        # print(response.text)
    else:
        print("Error:", response.status_code, response.text)


if __name__ == "__main__":
    print(get_joke(3))