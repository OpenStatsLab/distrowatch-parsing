import os
import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime

def save_news_json_to_file(json_data, file_path):
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as file:
            file.write(json_data)
        print('JSON data saved to {file_path}')
    except IOError:
        print('Failed to save JSON data to file.')

def get_news_items_as_json(url):
    base_url = 'https://distrowatch.com/?newsid='
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'lxml')

        news_items = []
        items = soup.find_all('item')
        for item in items:
            title = item.find('title').text.strip()
            full_link = item.find('link').text.strip()

            # Extract the necessary part of the link
            remaining_link = full_link.replace('https://distrowatch.com/', '')

            # Construct the complete URL
            complete_url = base_url + remaining_link

            date_str = item.find('dc:date').text.strip()

            # Get description from the constructed URL
            news_response = requests.get(complete_url)
            if news_response.status_code == 200:
                news_soup = BeautifulSoup(news_response.content, 'html.parser')
                description = news_soup.find('td', class_='NewsText').get_text().strip()
                description = description.replace('"', "'")  # Replace double quotes with single quotes
            else:
                description = 'Description not available'

            # Convert date string to datetime object
            date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S%z')

            # Convert datetime object to the desired date format
            formatted_date = date_obj.strftime('%d/%m/%Y, %H:%M')

            news_item = {
                'title': title,
                'link': full_link,
                'description': description,
                'date': formatted_date
            }
            news_items.append(news_item)

        json_data = json.dumps(news_items, indent=4)
        return json_data
    else:
        return None

xml_url = 'https://distrowatch.com/news/dw.xml'
json_news = get_news_items_as_json(xml_url)
if json_news:
    save_news_json_to_file(json_news, 'parsed/news.json')
else:
    print('Failed to fetch XML data.')
