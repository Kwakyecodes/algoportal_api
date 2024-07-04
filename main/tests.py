'''Unit tests for API endpoints'''


import json 

from rest_framework.test import APITestCase
from rest_framework import status


class RecordsCrudTestCase(APITestCase):
    full_body = {
        'call': 'exampleCall',
        'query': 'exampleQuery',
        'status': 'exampleStatus',
        'reason': 'exampleReason'
    }
    
    url = '/api/records/'
    
    def create_temp_id(self) -> int:
        '''Creates a temporay records object and returns it's id
        
        No arguments
        
        Returns:
            int: id of temporary records object
        '''
        temp_post = self.client.post(self.url, self.full_body)
        temp_provider = self.client.get(self.url)
        return temp_provider.json()[0]['id']
    
    def test_valid_post_with_full_body(self):
        response = self.client.post(self.url, self.full_body)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_valid_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_valid_put(self):
        response = self.client.put(self.url + f'{self.create_temp_id()}/', self.full_body)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_valid_delete(self):
        response = self.client.delete(self.url + f'{self.create_temp_id()}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        
class FetchCodeTestCase(APITestCase):
    body = {
        'query': 'python bubble sort implementation'
    }
    wrong_body = {
        'not_query': 'body of not_query'
    }
    url = '/api/fetch-code/'
    
    def test_valid_post(self):
        response = self.client.post(self.url, json.dumps(self.body), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
    def test_invalid_post(self):
        response = self.client.post(self.url, json.dumps(self.wrong_body), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        
class FetchDebuggerTestCase(APITestCase):
    body = {
        'error': 'permissions are too open'
    }
    wrong_body = {
        'not_error': 'body of not_error'
    }
    url = '/api/fetch-debugger/'
    
    def test_valid_post(self):
        response = self.client.post(self.url, json.dumps(self.body), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
    def test_invalid_post(self):
        response = self.client.post(self.url, json.dumps(self.wrong_body), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)