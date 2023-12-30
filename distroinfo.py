import requests
from bs4 import BeautifulSoup
import json
import os

def save_distro_info_to_file(json_data, file_path):
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as file:
            file.write(json_data)
        print(f"JSON data saved to {file_path}")
    except IOError:
        print("Failed to save JSON data to file.")

def get_distro_os_type(distro_url):
    response = requests.get(distro_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        os_type = soup.find('b', string='OS Type:')
        if os_type:
            a_tag = os_type.find_next('a')
            if a_tag:
                return a_tag.text.strip()
            else:
                return 'N/A'
        else:
            return 'N/A'
    else:
        print(f"Failed to fetch OS Type for {distro_url}")
        return 'N/A'

def update_distro_os_types(distro_options):
    for distro in distro_options:
        os_type = get_distro_os_type(distro['url'])
        distro['os_type'] = os_type

    return distro_options

def get_distro_options(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        select_list = soup.find('select', {'name': 'distribution'})
        if select_list:
            options = select_list.find_all('option')
            distro_info = []
            for option in options:
                if option.text.strip() != 'Select Distribution':
                    distro_name = option.text.strip()
                    codename = option.get('value')
                    url = "https://distrowatch.com/table.php?distribution=" + codename
                    imgurl = "https://distrowatch.com/images/yvzhuwbpy/" + codename + ".png"
                    distro_info.append({"distro": distro_name, "codename": codename, "url": url, "logo": imgurl})
            return distro_info
        else:
            print("Select list with name 'distribution' not found.")
            return None
    else:
        print("Failed to fetch the website.")
        return None

distrowatch_url = "https://distrowatch.com/"
distro_options = get_distro_options(distrowatch_url)
if distro_options:
    distro_options_with_os = update_distro_os_types(distro_options)
    if distro_options_with_os:
        json_data = json.dumps(distro_options_with_os, indent=4)
        save_distro_info_to_file(json_data, "parsed/distroinfo.json")
    else:
        print("No OS Type data to save.")
else:
    print("No data to save.")
