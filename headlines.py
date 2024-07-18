import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime
import os
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.3'}
def save_news_headlines_to_file(json_data, file_path):
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as file:
            file.write(json_data)
        print(f"JSON data saved to {file_path}")
    except IOError:
        print("Failed to save JSON data to file.")

def parse_news_headlines_xml(url):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'lxml')

        news_headlines = []
        items = soup.find_all('item')
        for item in items:
            title = item.find('title').text.strip()
            print(title)
            link = item.find('link').text.strip()
            pub_date = item.find('pubDate').text.strip()
            pub_date_obj = datetime.strptime(pub_date, "%a, %d %b %Y %H:%M:%S %z")
            formatted_pub_date = pub_date_obj.strftime('%d/%m/%Y, %H:%M')

            # Fetching contents from the provided link
            content_response = requests.get(link)
            if content_response.status_code == 200:
                content_soup = BeautifulSoup(content_response.content, 'html.parser')
                content = content_soup.find('td', {'valign': 'top'}).get_text().strip()
            else:
                content = "Content not available"

            news_headline = {
                "title": title,
                "link": link,
                "pub_date": formatted_pub_date,
                "content": content
            }
            news_headlines.append(news_headline)

        return news_headlines
    else:
        print("Failed to fetch XML data.")
        return None

xml_url = "https://distrowatch.com/news/news-headlines.xml"
news_headlines = parse_news_headlines_xml(xml_url)
if news_headlines:
    json_data = json.dumps(news_headlines, indent=4)
    save_news_headlines_to_file(json_data, "parsed/news_headlines.json")
else:
    print("No data to save.")
