"""
Rate Limiting Decorator for API Views
Protects against brute force attacks
"""
from functools import wraps
from django.core.cache import cache
from django.http import JsonResponse
from rest_framework import status


def rate_limit(key_func=None, rate='10/m', scope=None):
    """
    Rate limiting decorator.
    
    Usage:
        @rate_limit(rate='5/m', scope='login')
        def post(self, request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(self, request, *args, **kwargs):
            # Get client identifier (IP or user)
            if key_func:
                client_id = key_func(request)
            else:
                client_id = get_client_ip(request)
            
            # Build cache key
            scope_name = scope or view_func.__name__
            cache_key = f'ratelimit:{scope_name}:{client_id}'
            
            # Parse rate (e.g., '10/m' means 10 requests per minute)
            try:
                count, period = rate.split('/')
                count = int(count)
                period_map = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}
                period_seconds = period_map.get(period, 60)
            except (ValueError, KeyError):
                count, period_seconds = 10, 60
            
            # Check rate limit
            current = cache.get(cache_key, 0)
            if current >= count:
                return JsonResponse({
                    'success': False,
                    'data': None,
                    'meta': None,
                    'errors': [{
                        'code': 'RATE_LIMIT_EXCEEDED',
                        'field': None,
                        'message': 'تعداد درخواست‌های شما بیش از حد مجاز است. لطفاً چند لحظه صبر کنید.'
                    }]
                }, status=status.HTTP_429_TOO_MANY_REQUESTS)
            
            # Increment counter
            cache.set(cache_key, current + 1, period_seconds)
            
            return view_func(self, request, *args, **kwargs)
        
        return _wrapped_view
    return decorator


def get_client_ip(request):
    """Extract client IP from request, considering proxies."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    x_real_ip = request.META.get('HTTP_X_REAL_IP')
    if x_real_ip:
        return x_real_ip
    return request.META.get('REMOTE_ADDR', 'unknown')
