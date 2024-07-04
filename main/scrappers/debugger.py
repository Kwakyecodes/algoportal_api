''' Scrap multiple sets of codes from stackoverflow related with a given 
error message - https://stackoverflow.com/
'''


import re
from typing import List, Tuple, Dict
from concurrent.futures import ProcessPoolExecutor

from bs4 import BeautifulSoup

from .shared import (
    get_data,
    COMMENTS,
    LANGUAGES,
)


def get_links(error_msg: str) -> List[str]:
    '''Gets links to Stack Overflow sites related with 
    error_msg and returns them
    
    Arguments:
        error_msg: Error message
        
    Returns:
        List[str]: Stack Overflow links that are related to error_msg
    '''
    error_msg = error_msg.replace('+', '%2B') # For queries containing c++ language
    error_msg = error_msg.replace('#', '%23') # For queries containing c# language
    error_msg = error_msg.replace(' ', '+')
    google = 'https://www.google.com/search?q=stack+overflow+' + error_msg
    html = get_data(url=google)
    
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all('a')

    pattern = 'https://stackoverflow.com/q/[0-9]+|https://stackoverflow.com/questions/[0-9]+/[0-z,-]+'
    stack_links = []
    for link in links:
        result = re.findall(pattern, f'{link}')
        if result:
            stack_links.append(result[0])
            
    return stack_links


def fetch_comment_strings(error_msg: str) -> Tuple[str]:
    '''Finds the proper type of commenting needed for the language being used
    
    Arguments:
        error_msg: Error message
        
    Returns:
        Tuple[str]: A tuple containing the prefix and suffix that 
        makes a given line a comment
    '''
    for word in error_msg:
        if word in COMMENTS:
            return COMMENTS[word][0], COMMENTS[word][1]
    return 'COMMENT- ', ''


def generate_debugs(url: str, error_msg: str) -> List[str]:
    '''Scrapes question and answers from stackoverflow page
    
    Arguments:
        url: URL of the Stack Overflow site to be scraped
        error_msg: Error message
        
    Returns:
        List[str]: List containing scraped question and answer(s)
    '''
    complete_html_article = get_data(url=url)
    comment_beginning, comment_end = fetch_comment_strings(error_msg=error_msg)
    
    soup = BeautifulSoup(complete_html_article, 'html.parser')
    posts = soup.find_all('div', class_='s-prose js-post-body')
    processed_posts = []
    
    for post in posts:
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
                
            processed_posts.append(code)
            
    return processed_posts


def threader(error_msg: str) -> Dict[str, List[str]]:
    '''Threads the scrapping of questions and answers from stackoverflow page
    
    Arguments:
        error_msg: Error message
        
    Returns:
        Dict[str, List[str]]: Dictionary containing questions as key and 
        a list of their related solutions as their values
        Example: {
            "question1": [answer1, answer12, ...],
            "question2": [answer2, answer22, ....]
        }
    '''
    error_msg = error_msg.lower()
    urls = get_links(error_msg=error_msg)
    error_msgs = [error_msg for _ in range(len(urls))] # match length of urls to allow for use of map
    
    if not urls:
        return {}
    
    possible_solutions = {}
    with ProcessPoolExecutor() as execute:
        results = execute.map(generate_debugs, urls, error_msgs)

        for result in results:
            possible_solutions[result[0]] = result[1:]
    
    return possible_solutions