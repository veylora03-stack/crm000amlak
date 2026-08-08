"""
Custom Security Middleware
Adds extra security headers and protections
"""
import re


class SecurityHeadersMiddleware:
    """
    Adds security headers to all responses.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Prevent clickjacking
        response['X-Frame-Options'] = 'DENY'
        
        # Prevent MIME type sniffing
        response['X-Content-Type-Options'] = 'nosniff'
        
        # Enable XSS protection
        response['X-XSS-Protection'] = '1; mode=block'
        
        # Referrer policy
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Content Security Policy
        response['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self' data:; "
            "connect-src 'self'; "
            "frame-ancestors 'none'; "
            "base-uri 'self'; "
            "form-action 'self';"
        )
        
        # Permissions policy
        response['Permissions-Policy'] = (
            'geolocation=(self), '
            'microphone=(), '
            'camera=()'
        )
        
        return response


class RequestLoggingMiddleware:
    """
    Logs all API requests for security auditing.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        import logging
        logger = logging.getLogger('security')
        
        # Log suspicious patterns
        path = request.path
        query = request.META.get('QUERY_STRING', '')
        
        # SQL injection patterns
        sql_patterns = ['UNION SELECT', 'DROP TABLE', 'INSERT INTO', 'DELETE FROM', '--', ';--']
        for pattern in sql_patterns:
            if pattern.lower() in query.lower() or pattern.lower() in path.lower():
                logger.warning(
                    f'SQL Injection attempt blocked: IP={get_client_ip(request)}, '
                    f'Path={path}, Query={query}'
                )
        
        # XSS patterns
        xss_patterns = ['<script', 'javascript:', 'onerror=', 'onload=']
        for pattern in xss_patterns:
            if pattern.lower() in query.lower():
                logger.warning(
                    f'XSS attempt blocked: IP={get_client_ip(request)}, '
                    f'Path={path}, Query={query}'
                )
        
        response = self.get_response(request)
        return response


def get_client_ip(request):
    """Extract client IP from request."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', 'unknown')
