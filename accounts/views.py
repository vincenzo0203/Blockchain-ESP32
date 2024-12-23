# backend/accounts/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Person

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirect alla dashboard
        else:
            messages.error(request, 'Credenziali non valide!')
    
    return render(request, 'accounts/login.html')

@login_required
def dashboard_view(request):
    people = Person.objects.all()
    return render(request, 'accounts/dashboard.html', {'people': people})

@login_required
def person_add(request):
    if request.method == 'POST':
        rfid = request.POST.get('rfid')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        person = Person.objects.create(
            rfid=rfid,
            first_name=first_name,
            last_name=last_name
        )
        return JsonResponse({'person': {
            'id': person.id,
            'rfid': person.rfid,
            'first_name': person.first_name,
            'last_name': person.last_name
        }})

@login_required
def person_edit(request, pk):
    if request.method == 'POST':
        person = get_object_or_404(Person, pk=pk)
        person.rfid = request.POST.get('rfid')
        person.first_name = request.POST.get('first_name')
        person.last_name = request.POST.get('last_name')
        person.save()
        return JsonResponse({'person': {
            'id': person.id,
            'rfid': person.rfid,
            'first_name': person.first_name,
            'last_name': person.last_name
        }})

@login_required
def person_delete(request, pk):
    if request.method == 'POST':
        person = get_object_or_404(Person, pk=pk)
        person.delete()
        return JsonResponse({'status': 'success'})