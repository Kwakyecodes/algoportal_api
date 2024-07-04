''' Constants and helper functions for this project '''


import requests
import urllib3


urllib3.disable_warnings() # Disable warnings


LANGUAGES = (
    'python', 
    'python3', 
    'java', 
    'c++', 
    'c#', 
    'c', 
    'ruby', 
    'javascript', 
    'go', 
    'golang', 
    'rust', 
    'scheme', 
    'kotlin', 
    'sql',
    'r', 
    'swift', 
    'php', 
    'lua', 
    'html', 
    'css', 
    'typescript', 
    'perl', 
    'scala', 
    'matlab'
    )

COMMENTS = { # {language: [front_string, back_string]}
    'python':['# ', ''],
    'python3':['# ', ''],
    'c':['// ', ''],
    'c++':['// ', ''],
    'java':['// ', ''],
    'c#':['// ', ''],
    'ruby':['# ',''],
    'javascript':['// ',''],
    'go':['// ', ''],
    'golang':['// ', ''],
    'rust':['// ', ''],
    'scheme':['; ', ''],
    'kotlin':['// ', ''],
    'sql':['/* ', ' */'],
    'r':['# ', ''],
    'swift':['// ', ''],
    'php':['// ', ''],
    'lua':['-- ', ''],
    'html':['<!-- ', ' -->'],
    'css':['/* ', ' */'],
    'typescript':['/** ', '*/'],
    'perl':['# ', ''],
    'scala':['// ', ''],
    'matlab':['% ', '']
    }


def get_data(url: str) -> str:
    '''Makes request to fetch complete hmtl article and return it
    
    Arguments:
        url: URL of site to be scraped
    
    Returns:
        str: complete html article of url
    ''' 
    r = requests.get(url, verify=False)
    return r.text

