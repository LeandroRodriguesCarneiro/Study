from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib import auth

def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    elif request.method == 'POST':
        user_name = request.POST.get('username')
        password = request.POST.get('senha')
        confirm_password = request.POST.get('confirmar_senha')

        if not password or not confirm_password:
            messages.add_message(request, constants.ERROR, 'precisa cadastrar uma senha')
            return redirect('/users/register')

        if not password == confirm_password:
            messages.add_message(request, constants.ERROR, 'Senha e confirma senha nao coicidem')
            return redirect('/users/register')
        
        if User.objects.filter(username = user_name).exists():
            messages.add_message(request, constants.ERROR, 'Usuario ja existe')
            return redirect('/users/register')

        try:
            User.objects.create_user(
                username= user_name,
                password= password
            )
            messages.add_message(request, constants.SUCCESS, 'Registrado!!!')
            return redirect('/users/login')
        except:
            messages.add_message(request, constants.ERROR, 'Erro interno do servidor')
            return redirect('/users/register')

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        user_name = request.POST.get('username')
        password = request.POST.get('senha')

        user = auth.authenticate(request, username = user_name, password = password)
        if user:
            auth.login(request, user)
            messages.add_message(request, constants.SUCCESS, 'Logado!!!')
            return redirect('/flashcard/new_flashcard/')
        else:
            messages.add_message(request, constants.ERROR, 'Username ou senha invalidos')
            return redirect('/users/login')
        
def logout(request):
    auth.logout(request)
    return redirect('/users/login')