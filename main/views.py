import json
import math as m
from typing import List
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor, as_completed

from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest

from .models import Records
from .scrappers.geeks import generate_code_geeks
from .scrappers.stackoverflow import generate_code_stackoverflow
from .scrappers.w3 import generate_code_w3
from .scrappers.debugger import threader


### HELPER FUNCTIONS ###

def log_usage(call: str, status='Fail', query='Not given', reason='NA') -> None:
    '''Logs api usage into database
    
    Arguments:
        call: The api endpoint that was called
        status: Whether the call was successful or not
        query: User query
        reason: Reason why call failed. Not applicable if call was successful
        
    Returns None.
    '''
    record = Records(call=call, status=status, query=query, reason=reason, time=f'{datetime.now()}')
    record.save()
    
    
def preference(solution: str, query: str) -> int:
    '''Scores all solutions to see which one should appear first
    
    Arguments:
        solution: Solution to be evaluated
        query: User query
        
    Returns:
        int: Score of solution after evaluation
    '''
    query, solution = query.lower().split(' '), solution.lower()
    score = 0
    
    for key_word in query:
        if key_word in solution:
            score += len(key_word)
            
    if score > 0:
        return int(m.log(score)*1.5 + m.log(len(solution)))
    else:
        return int(m.log(len(solution) + 1)) # plus 1 is bias


def get_codes(query: str) -> List[str]:
    '''Fetches all codes from the various sites
    (Geeksforgeeks, Stack Overflow, W3schools) and returns them
    
    Arguments:
        query: User query
        
    Returns:
        List[str]: List of all scraped codes 
    '''
    all_solutions = []
    
    with ProcessPoolExecutor() as execute:
        results = []
        results.append(execute.submit(generate_code_geeks, query))
        results.append(execute.submit(generate_code_stackoverflow, query))
        results.append(execute.submit(generate_code_w3, query))
        
        for f in as_completed(results):
            all_solutions += f.result()
    
    all_solutions_dict = {solution: preference(solution, query) for solution in all_solutions}
    
    sorted_solutions = [key for key, val in sorted(all_solutions_dict.items(), key = lambda ele: ele[1], reverse = True)]
    
    return sorted_solutions


### API FUNCTIONS ###

@api_view(['POST'])
def fetch_code(request):
    '''End point that takes query and returns all related codes found from 
    stackoverflow, geeksforgeeks, codegrepper and w3schools
    
    Method: POST
    
    Accepts: Application/json
    '''
    if request.method == 'POST':
        data = json.loads(request.body)
        
        try:
            query = data['query']
        except:
            log_usage(call="Fetch-code", reason="Query was not found")
            return HttpResponseBadRequest('Body must contain a query')
        
        if not query:
            log_usage(call='Fetch-code', query=query, reason='Query is an empty string')
            return HttpResponseBadRequest('Query cannot be an empty string')
        
        codes = get_codes(query)
        log_usage(call='Fetch-code', status='Success', query=query)
        
        return JsonResponse(codes, safe=False)


@api_view(['POST'])
def fetch_debugger(request):
    '''End point that takes an error message and returns all 
    related codes from stackoverflow
    
    Method: POST
    
    Accepts: Application/json
    '''
    if request.method == 'POST':
        data = json.loads(request.body)
        
        try:
            error_msg = data['error']
        except:
            return HttpResponseBadRequest('Body must contain error message')
        
        if not error_msg:
            return HttpResponseBadRequest('Error message cannot be empty')
        
        debugs = threader(error_msg)
        
        return JsonResponse(debugs, safe=False)