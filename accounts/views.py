# backend/accounts/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Person
from django.core.paginator import Paginator
from blockchain.utils import log_admin_login_on_blockchain, log_admin_action_on_blockchain


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            log_admin_login_on_blockchain(username, True)
            login(request, user)
            return redirect('user_management')  # Redirect alla dashboard
        else:
            log_admin_login_on_blockchain(username, False)
            messages.error(request, 'Credenziali non valide!')
    
    return render(request, 'accounts/login.html')

@login_required
def user_management_view(request):
    people = Person.objects.all()
    
    paginator = Paginator(people, 10)

    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    response = render(request, 'accounts/user_management.html', {'people': page_obj})
    
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    
    return response

@login_required
def user_access_view(request):

    response = render(request, 'accounts/user_access.html')
    
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    
    return response

@login_required
def admin_access_view(request):

    response = render(request, 'accounts/admin_access.html')
    
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    
    return response

@login_required
def person_add(request):
    if request.method == 'POST':
        rfid = request.POST.get('rfid')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        admin = request.user.username
        

        person = Person.objects.create(
            rfid=rfid,
            first_name=first_name,
            last_name=last_name
        )
        
        log_admin_action_on_blockchain(admin,"Inserimento", rfid)

        return JsonResponse({'person': {
            'id': person.id,
            'rfid': person.rfid,
            'first_name': person.first_name,
            'last_name': person.last_name
        }})

@login_required
def person_edit(request):
    if request.method == 'POST':
        admin = request.user.username
        id = request.POST.get('id')
        person = get_object_or_404(Person, pk=id)
        #person.rfid = request.POST.get('rfid')
        person.first_name = request.POST.get('first_name')
        person.last_name = request.POST.get('last_name')
        person.save()
        log_admin_action_on_blockchain(admin,"Modifica", person.rfid)
        return JsonResponse({'person': {
            'id': person.id,
            'rfid': person.rfid,
            'first_name': person.first_name,
            'last_name': person.last_name
        }})

@login_required
def person_delete(request):
    if request.method == 'POST':
        admin = request.user.username
        id = request.POST.get('id')
        person = get_object_or_404(Person, pk=id)
        log_admin_action_on_blockchain(admin,"Eliminazione", person.rfid)
        person.delete()
        return JsonResponse({'status': 'success'})

def custom_404(request, exception):
    return render(request, 'errorPage/404.html', status=404)