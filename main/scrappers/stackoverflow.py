''' Scrap code from stackoverflow - https://stackoverflow.com/ '''


import re
from typing import List, Tuple

from bs4 import BeautifulSoup

from .shared import (
    COMMENTS,
    LANGUAGES,
    get_data,
)


def get_link(query: str) -> str:
    '''Gets link to stack overflow and returns it
    
    Arguments:
        query: User query
        
    Returns:
        str: Stack Overflow link related to query
    '''
    query = query.replace('+', '%2B') # For queries containing c++ language
    query = query.replace('#', '%23') # For queries containing c# language
    query = query.replace(' ', '+')
    google = 'https://www.google.com/search?q=stack+overflow+' + query
    html = get_data(url=google)
    
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all('a')

    pattern = 'https://stackoverflow.com/q/[0-9]+|https://stackoverflow.com/questions/[0-9]+/[0-z,-]+'
    for link in links:
        result = re.findall(pattern, f'{link}')
        if result:
            return result[0]
    
    return ''

def fetch_comment_strings(query: str) -> Tuple[str]:
    '''Finds the proper type of commenting needed for the language being used
    
    Arguments:
        query: User query
        
    Returns:
        Tuple[str]: A tuple containing the prefix and suffix that 
        makes a given line a comment
    '''
    for word in query.split(" "):
        if word in COMMENTS:
            return COMMENTS[word][0], COMMENTS[word][1]
    return 'COMMENT- ', ''


def generate_code_stackoverflow(query: str) -> List[str]:
    '''Scrapes code from stackoveflow url and returns list of codes
    
    Arguments:
        query: User query
        
    Returns:
        List[str]: List of scraped codes
    '''
    query = query.lower()
    url = get_link(query=query)
    if not url:  # No stackoverflow urls found for the query
        return []
    
    complete_html_article = get_data(url=url)
    soup = BeautifulSoup(complete_html_article, 'html.parser')
    posts = soup.find_all('div', class_='s-prose js-post-body')
    
    comment_beginning, comment_end = fetch_comment_strings(query=query)
    
    answers = []
    
    for ind, post in enumerate(posts):
        code = ''
        for line in post:
            line_str = f'{line}'
            if line_str == '\n':
                continue
            
            if '<p>' in line_str:
                code += comment_beginning
                code += line.get_text().replace('\n', comment_end + '<br>' + comment_beginning) + comment_end + '<br>'
            else:
                code += line.get_text().replace('\n', '<br>') + '<br>'
            
        if ind > 0:
            answers.append(code)
            
    return answers


