# Debug middleware để log CSRF errors
import logging

logger = logging.getLogger(__name__)

class CSRFDebugMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if 'CSRF' in str(exception):
            logger.error(f"CSRF Error: {exception}")
            logger.error(f"Request method: {request.method}")
            logger.error(f"Request path: {request.path}")
            logger.error(f"User: {request.user}")
            logger.error(f"Session key: {request.session.session_key}")
        return None
