from rest_framework.views import exception_handler
from rest_framework.response import Response

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    
    if response is not None:
        custom_response_data = {
            'success': False,
            'data': None,
            'meta': None,
            'errors': []
        }
        
        if isinstance(response.data, dict):
            for key, value in response.data.items():
                if key == 'detail':
                    custom_response_data['errors'].append({
                        'code': 'ERROR',
                        'field': None,
                        'message': str(value)
                    })
                elif isinstance(value, list):
                    for msg in value:
                        custom_response_data['errors'].append({
                            'code': 'VALIDATION_ERROR',
                            'field': key,
                            'message': str(msg)
                        })
                else:
                    custom_response_data['errors'].append({
                        'code': 'ERROR',
                        'field': key,
                        'message': str(value)
                    })
        elif isinstance(response.data, list):
            for msg in response.data:
                custom_response_data['errors'].append({
                    'code': 'ERROR',
                    'field': None,
                    'message': str(msg)
                })
        
        response.data = custom_response_data
    
    return response
