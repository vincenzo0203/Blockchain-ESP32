from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .utils import get_message, is_valid_uid
import json

def contract_message(request):
    try:
        message = get_message()
        return JsonResponse({"message": message})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def check_uid(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            uid = data.get('uid')
            print(uid)
            # Verifica UID utilizzando la funzione helper
            if is_valid_uid(uid):
                return JsonResponse({"status": "success", "access": True})
            else:
                return JsonResponse({"status": "success", "access": False})
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)
    return JsonResponse({"status": "error", "message": "Invalid method"}, status=405)