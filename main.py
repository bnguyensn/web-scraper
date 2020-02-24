import json
from pathlib import Path
import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup


def run(hashtag):
    url = f'https://www.instagram.com/explore/tags/{hashtag}/'

    try:
        response = requests.get(url, timeout=10.0)

        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        print(f'Successfully fetched Instagram data for hashtag {hashtag}!')

        soup = BeautifulSoup(response.content, 'html.parser')

        scripts = soup.find_all('script')

        # Post data is stored in the 3rd script
        json_string = (scripts[3].text[21:-1])

        json_obj = json.loads(json_string)

        hashtag_data = json_obj['entry_data']['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_top_posts']['edges']

        print(f'Length of hashtag_data: {len(hashtag_data)}')

        # Save to local file
        file_path = Path(f'data/{hashtag}.json')
        with open(file_path, 'w') as f:
            json.dump(hashtag_data, f)

        print(f'Successfully printed {file_path}')


run('beer')
