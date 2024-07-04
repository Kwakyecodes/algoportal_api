''' Scrap files from GeeksforGeeks - https://www.geeksforgeeks.org/ '''


import re
from typing import List, Tuple

from bs4 import BeautifulSoup

from .shared import (
    LANGUAGES, 
    get_data, 
    COMMENTS
)


def process(user_input: str) -> Tuple[str]:
    '''Processes user_input and extract query and programming language
    
    Arguments:
        user_input: User input
        
    Returns:
        Tuple[str]: Query and programming language extracted from
        user_input
    '''
    languages = LANGUAGES
    programming_language = ''
    
    for word in user_input.split(' '):
        if word in languages:
            programming_language = word
            break

    return user_input, programming_language


def get_link(query: str) -> str:
    '''Gets link to Geeks for Geeks site related to query and return it
    
    Arguments:
        query: User query
        
    Returns:
        str: Geeks for Geeks link related to query
    '''
    query = query.replace('+', '%2B') # For queries containing c++ language
    query = query.replace('#', '%23') # For queries containing c# language
    query = query.replace(' ', '+')
    google = 'https://www.google.com/search?q=geeks+for+geeks+' + query
    html = get_data(url=google)
    
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all('a')

    pattern = 'https://www.geeksforgeeks.org/[0-z,-]+/'
    for link in links:
        result = re.findall(pattern, f'{link}')
        if result:
            return result[0]
        
    return ''


def get_code_lines(hmtl_article: str) -> List[str]:
    '''Processses complete html article and extracts html lines 
    containing the code
    
    Arguments:
        html_article: Complete html article to be processed
        
    Returns:
        List[str]: List of code lines
    '''
    code_lines = re.findall('<div class="line number.+ index.+ alt.+">.+</div>', hmtl_article)
    code_lines = code_lines[0].split('</div>')
    return code_lines


def extract_text(code_line: str) -> str:
    '''Extracts actual text from html code lines
    
    Arguments:
        code_line: html line containg code
        
    Returns:
        str: actual code text extracted from html code line
    '''
    code = ''
    collect = False
    for char in code_line:
        if char == '>':
            collect = True
            continue
        elif char == '<':
            collect = False
            continue
            
        if collect:
            code += char
    
    return code


def generate_code_geeks(user_input: str) -> List[str]:
    '''Gets lines of code from url and return list of chunks of code
    
    Arguments:
        user_input: User input
        
    Returns:
        List[str]: List containing scrapped code from site related to
        user_input
    ''' 

    # process user_input into query and programming languages
    user_input = user_input.lower()
    query, programming_language = process(user_input=user_input)
    
    # Get url of geeksforgeeks link
    url = get_link(query=query)
    if not url:
        return []
    
    complete_article_html = get_data(url=url)
    soup = BeautifulSoup(complete_article_html, 'html.parser')
    
    # Get dictionary of languages and their appropriate indices
    languages = {}
    for ind, html_line in enumerate(soup.find_all('h2', class_='tabtitle')):
        lang = extract_text(f'{html_line}').lower()
        if lang in languages:
            languages[lang].append(ind)
        else:
            languages[lang] = [ind]
            
    # Get all codes into code_container
    code_container = soup.find_all('div', class_='code-container')
    
    # Check if there are any codes on that webpage
    if not code_container:
        return []
    
    solutions = []
    
    if not languages or not programming_language:
        for i in range(len(code_container)):
            code_lines = get_code_lines(hmtl_article=f'{code_container[i]}')
            solution = ''
            for line in code_lines:
                if 'class' in line:
                    code = extract_text(f'{line}')
                    solution += code + '<br>'
                    
            solution = solution.replace('&lt;', '<') # Fix < bug
            solution = solution.replace('&gt;', '>') # Fix > bug
            solutions.append(solution)
            
        return solutions
            
    # python and python3 should should be considered as the same language 
    if 'python' in languages and 'python' in programming_language:
        programming_language = 'python'
    elif 'python3' in languages and 'python' in programming_language:
        programming_language = 'python3'
    
    # Check if programming_language is among the available langauges
    if programming_language not in languages:
        return []
    
    # Get hmtl lines that contain the code text and extract the text into solutions
    for i in languages[programming_language]:
        code_lines = get_code_lines(hmtl_article=f'{code_container[i]}')
        solution = ''
        for line in code_lines:
            if 'class' in line:
                code = extract_text(f'{line}')
                solution += code + '<br>'
                
        solution = solution.replace('&lt;', '<') # Fix < bug
        solution = solution.replace('&gt;', '>') # Fix > bug
        solutions.append(solution)
    
    return solutions