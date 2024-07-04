''' Scrap code from w3schools - https://www.w3schools.com/ '''


import re
from typing import List

from bs4 import BeautifulSoup

from .shared import (
    COMMENTS,
    LANGUAGES,
    get_data,
)


def get_link(query: str) -> str:
    '''Gets link to w3schools site returns it
    
    Arguments:
        query: User query
        
    Returns:
        str: W3schools link related to query
    '''
    query = query.replace('+', '%2B') # For queries containing c++ language
    query = query.replace('#', '%23') # For queries containing c# language
    query = query.replace(' ', '+')
    google = 'https://www.google.com/search?q=w3schools+' + query
    html = get_data(url=google)
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all('a')

    pattern = 'https://www.w3schools.com/[0-z]+/[0-z,-,.]+'
    for link in links:
        result = re.findall(pattern, f'{link}')
        if result:
            break
    if result:
        return result[0]
    else:
        return ''
    

def generate_code_w3(query: str) -> List[str]:
    '''Scrapes code from url and returns them
    
    Arguments:
        query: User query
        
    Returns:
        List[str]: List of scraped codes
    '''
    query = query.lower()
    url = get_link(query=query)
    if not url:
        return []
    
    complete_html_article = get_data(url=url)
    
    soup = BeautifulSoup(complete_html_article, 'html.parser')
    posts = soup.find_all('div', {'class': re.compile(r'w3-code notranslate [a-z]+')})
    
    codes = []
    for post in posts:
        code = ''
        for line in post:
            buffer = line.get_text().replace('\n', '').replace('  ', '')
            if buffer: 
                code += buffer + '<br>'
            
        codes.append(code)
   
    return codes