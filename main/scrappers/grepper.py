''' Scrap codes from Code grepper - https://www.codegrepper.com/ '''


import re
from typing import List

import requests
import urllib3
from bs4 import BeautifulSoup

from .shared import (
    COMMENTS, 
    get_data, 
    LANGUAGES,
)


urllib3.disable_warnings() # Disable warnings


def get_data_from_codegrepper(url: str) -> str:
    '''Makes request to fetch complete hmtl article from codegrepper and return it
    
    Arguments:
        url: URL of codegrepper site
    
    Returns:
        str: complete html article of url
    ''' 
    
    cookies = {
    'G_AUTHUSER_H': '0',
    'G_ENABLED_IDPS': 'google',
    'cto_bundle': 'NYH8zV8yRW9rQnI0SG5tNW9iOVhzN3o0TlpIQVFEMkxEZFpEOWhZYUk5bVFTVk1sM2FjJTJGVmRWdUhBSWZPdUV5U3VhTlAwN09mSmlRNWJ1dlZPQ1ZTZm83VkxKeGZnTndZN0U1bGVRVVI4d2JhU1NoNVk2QzdkUlZ6VDhqMmp3SUpjWlBRM1RpTlFnNFNuclNCRUlPZ2ZHakswUSUzRCUzRA',
    'PHPSESSID': 'u8vefplmhedpd1tqihuhtr52be',
    'g_state': '{"i_l":1,"i_p":1651789476413}',
    '_ga': 'GA1.1.452698965.1631102241',
    'G_AUTHUSER_H': '0',
    '_ga_WFMBHFF6RZ': 'GS1.1.1651784040.1.1.1651785769.0',
    '__gads': 'ID=7898d4aa38527892:T=1631102240:S=ALNI_MYQ6JCshBHCFpdsBcjBge50fyANbQ',
    '__gpi': 'UID=000005d98ed2af36:T=1651785771:RT=1651785771:S=ALNI_Mao8IdQrc5j__HDw8nH6IqRTUeDsg',
    'grepper_web_access_token': '9f7c3670a1916322abef340f666a23c27e67e0a5f67f90cdb32c72f0293f581fb20b855c69bac5e8723096f884bf84821d1b20174b80027c0e6fd28f065dfe65',
    }
    
    headers = {
    'authority': 'www.codegrepper.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'referer': 'https://www.codegrepper.com/code-examples/java/print+method+in+java',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
    }
    
    r = requests.get(url, cookies=cookies, headers=headers, verify=False)
    return r.text


def get_link(query: str) -> str:
    '''Gets link to Code grepper site and returns it
    
    Arguments:
        query: User query
    
    Returns:
        str: link to code grepper site related with query
    '''
    query = query.replace('+', '%2B') # For queries containing c++ language
    query = query.replace('#', '%23') # For queries containing c# language
    query = query.replace(' ', '+')
    
    google = 'https://www.google.com/search?q=codegrepper+' + query
    html = get_data(url=google)
    
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all('a')
        
    pattern = 'https://www.codegrepper.com/code-examples/[a-z]+/[0-z,%,-,+]+'
    for link in links:
        result = re.findall(pattern, f'{link}')
        if result:
            return result[0].replace('%2B', '+').replace('25', '')
    
    return ''


def generate_code_codegrepper(query: str) -> List[str]:
    '''Scrapes code from codegrepper url
    
    Arguments:
        query: User query
        
    Returns:
        List[str]: List of scraped codes
    '''
    query = query.lower()
    url = get_link(query=query)
    
    if not url:
        return []

    complete_html_article = get_data_from_codegrepper(url=url)
    soup = BeautifulSoup(complete_html_article, 'html.parser')
    code_containers = soup.find_all('textarea')
    
    solutions = []
    for code in code_containers:
        solution = ''
        for line in code:
                solution += line.get_text() + '<br>'
        solutions.append(solution)
    
    return solutions