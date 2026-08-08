def success_response(data=None, meta=None):
    return {
        'success': True,
        'data': data,
        'meta': meta,
        'errors': []
    }


def error_response(errors, status=400):
    return {
        'success': False,
        'data': None,
        'meta': None,
        'errors': errors
    }, status
