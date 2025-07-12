from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def ai_page(request):
    """View để hiển thị trang AI Chatbot"""
    return render(request, 'AI_page/AI.html')

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
            
            # Placeholder response - sẽ được thay thế bằng AI thực tế
            response = {
                'status': 'success',
                'message': f'Đã nhận tin nhắn: {message}',
                'suggestion': 'Vui lòng cấu hình API key để sử dụng AI Assistant'
            }
            
            return JsonResponse(response)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'})
