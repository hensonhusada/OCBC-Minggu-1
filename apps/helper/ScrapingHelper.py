from bs4 import BeautifulSoup
from apps.schemas import BaseResponse
from apps.helper import Log
import requests, re
import datetime
import pandas as pd

# For debugging purposes
# headers = {
#     "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Mobile Safari/537.36",
#     "Accept-Language": "en-US,en;q=0.9,id;q=0.8,ms;q=0.7,ja;q=0.6,ko;q=0.5"
#     }
# base_url = 'https://www.psychologytoday.com/intl/blog-posts?page='

# Fetch website & return its text/content
def get_web_content(url, headers):    
    cap_data = requests.get(url, headers=headers)
    return cap_data.text

# Return resultset of desired tags & class in texts with BeautifulSoup parser
def get_bs4_containers(url, headers, parser: str, tag:str, class_: str):
    cap_data = get_web_content(url, headers)
    soup = BeautifulSoup(cap_data, parser)
    containers = soup.find_all(tag, class_=class_)
    return containers

# Get one page of records from psychologytoday.com and return
# the articles' information
def get_one_page_psycho(page_num):
    def clean_date():
        date = re.findall(
            r'([A-Za-z]\w+ [0-9]\d{0,1}, [0-9]\d{3})',
            content.p.text
        )[0]\
            .replace(',', '')
        return date

    response = BaseResponse()
    results = []
    base_url = 'https://www.psychologytoday.com/intl/blog-posts?page='
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Mobile Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9,id;q=0.8,ms;q=0.7,ja;q=0.6,ko;q=0.5"
    }
    url = base_url + str(page_num-1)
    Log.info("Fetching"+url)
    try:
        soup_results = get_bs4_containers(
            url, headers, 'html.parser', 'div', class_='blog_entry__text'
        )            
        
        for content in soup_results:
            temp = 'https://psychologytoday.com' + content.h2.a['href']
            results.append({
                'title': content.h2.a.text,
                'genre': content.h6.text,
                'publisher': content.p.a.text,
                'publishdate': pd.to_datetime(clean_date()),
                'magazine': content.p.find_all('a')[1].text,
                'url': temp,
                'summary': content.find('p', class_='blog_entry__teaser d-none d-sm-block').text
            })
            
        response.status = 200
        response.message = "Success"
        response.data = results
    except Exception as e:
        Log.error(e)
        response.status = 404
        response.message = "Not Found"

    return response