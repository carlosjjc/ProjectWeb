from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import *
from .forms import ApostaForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from decimal import Decimal

def post_list(request):
    return render(request,'blog/post_list.html',{'Jogador':Jogador.objects.all(),'Time':Time.objects.all()})

def apostar(request):
    if request.method == 'POST':
        form = ApostaForm(request.POST)
        if form.is_valid():
            aposta = form.save(commit=False)
            if str(request.user) == 'AnonymousUser':
                print('Fazer login')
                return redirect('/login',{})
            elif(Jogador.objects.filter(id=request.user)):
                usuario = Jogador.objects.filter(id=request.user)[0]
                if Aposta.objects.filter(id_jogador=usuario,id_partida = aposta.id_partida) or usuario.saldo < 5:
                    print('Partida ja cadastrada')
                else:
                    valor = usuario.saldo
                    valor = valor - 5
                    usuario.saldo = valor
                    usuario.save()
                    aposta.id_jogador = usuario
                    aposta.save()
                    return HttpResponseRedirect('/')
            
    form = ApostaForm()
    return render(request,'blog/apostar.html',{'aposta':form})

def initialize(request):
    partida = Partida.objects.all()
    return render(request,'blog/inicio.html',{'partida':partida})

def ranking(request):
    jogador = Jogador.objects.all()
    return render(request,'blog/ranking.html',{'jogador':jogador})

def resultado(request):
    jogador = Jogador.objects.all()
    return render(request,'blog/resultado.html',{'jogador':jogador})

def cadastro(request):
    if request.POST:
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        email=request.POST['email']
        username=request.POST['username']
        password=request.POST['password']
        print('Usuario',username,'Senha',password)
        if User.objects.filter(username=request.POST['username']):
            print('Usuario ja cadastrado')
        else:
            user = User.objects.create_user(first_name=first_name,
                                    last_name=last_name,
                                    email=email,
                                    username=username,
                                    password=password)
            if not Jogador.objects.filter(id=user):
                Jogador.objects.create(id=user)
                return redirect('/login',{})
    return render(request,'blog/cadastro.html',{})

def autenticar(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        print('Usuario',username,'Senha',password)
        
        user = authenticate(username=username, password=password)
        print(user)
        if user:
            login(request, user)
            return HttpResponseRedirect('/')
    return render(request,'blog/login.html')

def deslogar(request):
    logout(request)
    return render(request,'blog/inicio.html')

# Create your views here.
