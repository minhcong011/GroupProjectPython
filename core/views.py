from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib.auth.decorators import login_required
import json
from core.models import Account

# Create your views here.

@login_required
def get_groq_config(request):
    """
    Safely provide Groq API configuration to authenticated users
    """
    if request.method == 'GET':
        try:
            # Only provide API key to authenticated users
            if request.user.is_authenticated:
                api_key = getattr(settings, 'GROQ_API_KEY', '')
                if not api_key:
                    # Fallback to environment variable or default
                    import os
                    api_key = os.environ.get('GROQ_API_KEY', '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')
                
                return JsonResponse({
                    'api_key': api_key,
                    'api_url': 'https://api.groq.com/openai/v1/chat/completions',
                    'model_name': 'llama-3.1-8b-instant',
                    'success': True
                })
            else:
                return JsonResponse({
                    'error': 'Authentication required',
                    'success': False
                }, status=401)
        except Exception as e:
            return JsonResponse({
                'error': f'Configuration error: {str(e)}',
                'success': False
            }, status=500)
    
    return JsonResponse({
        'error': 'Method not allowed',
        'success': False
    }, status=405)
