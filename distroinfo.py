import requests
from bs4 import BeautifulSoup
import json
import os

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.3'}

def in_between(string,x,y):
    return string[string.index(x)+1:string.index(y)]

def save_distro_info_to_file(json_data, file_path):
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as file:
            file.write(json_data)
        print(f"JSON data saved to {file_path}")
    except IOError:
        print("Failed to save JSON data to file.")

def get_distro_info(distro_url):
    response = requests.get(distro_url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        os_type = soup.find('b', string='OS Type:')
        if os_type:
            a_tag = os_type.find_next('a')
            if a_tag:
                os_type_value = a_tag.text.strip()
            else:
                os_type_value = 'N/A'
        else:
            os_type_value = 'N/A'

        homepage = 'N/A'
        th_home_page = soup.find('th', string='Home Page')
        if th_home_page:
            td_next = th_home_page.find_next('td')
            if td_next and td_next.a:
                homepage = td_next.a.get('href')
        
        return os_type_value, homepage
    else:
        print(f"Failed to fetch distro information for {distro_url}")
        return 'N/A', 'N/A', 'N/A'

def get_distro_options(url):
    response = requests.get(url, headers=headers)
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
                    scrurl = "https://distrowatch.com/images/ktyxqzobhgijab/" + codename + ".png"
                    os_type, homepage = get_distro_info(url)
                    distro_info.append({
                        "distro": distro_name,
                        "codename": codename,
                        "url": url,
                        "logo": imgurl,
                        "screenshot": scrurl,
                        "homepage": homepage,
                        "ostype": os_type
                    })
                    print(distro_info)
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
    json_data = json.dumps(distro_options, indent=4)
    save_distro_info_to_file(json_data, "parsed/distroinfo.json")
else:
    print("No data to save.")
