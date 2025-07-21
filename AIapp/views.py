from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json

def ai_page(request):
    """View để hiển thị trang AI Chatbot"""
    context = {}
    
    # Chỉ cung cấp API key cho authenticated users
    if request.user.is_authenticated:
        # Lấy API key từ settings
        api_key = getattr(settings, 'GROQ_API_KEY', '')
        if not api_key:
            # Fallback to environment variable
            import os
            api_key = os.environ.get('GROQ_API_KEY', '')
        
        context['groq_api_key'] = api_key
    
    return render(request, 'AI_page/AI.html', context)

def setup_guide(request):
    """Trang hướng dẫn cấu hình API"""
    return render(request, 'AI_page/setup_guide.html')

@csrf_exempt
def chat_api(request):
    """API endpoint cho chat (có thể mở rộng sau)"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message = data.get('message', '')
            
            response = {
                'status': 'success',
                'message': f'Đã nhận tin nhắn: {message}',
                'suggestion': 'Vui lòng cấu hình API key để sử dụng AI Assistant'
            }
            return JsonResponse(response)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'})
