import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime
import os

def save_distributions_json_to_file(json_data, file_path):
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as file:
            file.write(json_data)
        print(f"JSON data saved to {file_path}")
    except IOError:
        print("Failed to save JSON data to file.")

def parse_distributions_xml(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'lxml')

        distributions = []
        items = soup.find_all('item')
        for item in items:
            title = item.find('title').text.strip()
            # Splitting the title into date, distro name, and version
            date_str, rest = title.split(' ', 1)
            date_obj = datetime.strptime(date_str, "%m/%d")
            distro, version = rest.rsplit(' ', 1)

            distribution = {
                "date": date_obj.strftime('%d/%m'),
                "distro_name": distro,
                "version": version
            }
            distributions.append(distribution)

        return distributions
    else:
        print("Failed to fetch XML data.")
        return None

xml_url = "https://distrowatch.com/news/dwd.xml"
distributions = parse_distributions_xml(xml_url)
if distributions:
    json_data = json.dumps(distributions, indent=4)
    save_distributions_json_to_file(json_data, "parsed/distroreleases.json")
else:
    print("No data to save.")
