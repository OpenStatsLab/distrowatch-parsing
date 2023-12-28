import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime
import os

def save_package_releases_to_file(json_data, file_path):
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as file:
            file.write(json_data)
        print(f"JSON data saved to {file_path}")
    except IOError:
        print("Failed to save JSON data to file.")

def parse_package_releases_xml(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'xml')

        package_releases = []
        items = soup.find_all('item')
        for item in items:
            title = item.find('title').text.strip()
            # Splitting the title into date, package name, and version
            date_str, rest = title.split(' ', 1)
            date_obj = datetime.strptime(date_str, "%m/%d")
            package, version = rest.rsplit(' ', 1)

            link = item.find('link').text.strip()

            package_release = {
                "date": date_obj.strftime('%d/%m'),  # Modified to a more readable date format
                "package_name": package,
                "version": version,
                "link": link  # Added link item
            }
            package_releases.append(package_release)

        return package_releases
    else:
        print("Failed to fetch XML data.")
        return None

xml_url = "https://distrowatch.com/news/dwp.xml"
package_releases = parse_package_releases_xml(xml_url)
if package_releases:
    json_data = json.dumps(package_releases, indent=4)
    save_package_releases_to_file(json_data, "parsed/packagereleases.json")
else:
    print("No data to save.")
