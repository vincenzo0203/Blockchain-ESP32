from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .utils import is_valid_uid, log_access_on_blockchain, get_access_logs, get_access_admin_logs, get_admin_action_logs
from django.contrib.auth.decorators import login_required
import json

@csrf_exempt
def check_uid(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            uid = data.get("uid")

            if not uid:
                return JsonResponse({"error": "UID non fornito"}, status=400)

            access_granted = is_valid_uid(uid)  # Controlla se l'UID è valido

            if access_granted:
                tx_hash = log_access_on_blockchain(uid, access_granted)
                return JsonResponse({"status": "success", "access": True})
            else:
                tx_hash = log_access_on_blockchain(uid, access_granted)
                return JsonResponse({"status": "success", "access": False})
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)
    return JsonResponse({"status": "error", "message": "Invalid method"}, status=405)

@csrf_exempt
@login_required
def get_logs(request):
    """Restituisce tutti i log degli accessi registrati sulla blockchain"""
    if request.method == 'GET':
        logs = get_access_logs()
        return JsonResponse({"logs": logs})

    return JsonResponse({"error": "Metodo non consentito"}, status=405)

@csrf_exempt
@login_required
def get_admin_login_logs(request):
    """Restituisce tutti i log dei login amministrativi registrati sulla blockchain"""
    if request.method == 'GET':
        try:
            logs = get_access_admin_logs()
            return JsonResponse({"logs": logs}, safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Metodo non consentito"}, status=405)

@csrf_exempt
@login_required
def get_admin_action_logs_view(request):
    """Restituisce tutti i log delle azioni amministrative registrati sulla blockchain"""
    if request.method == 'GET':
        try:
            logs = get_admin_action_logs()
            return JsonResponse({"logs": logs}, safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Metodo non consentito"}, status=405)