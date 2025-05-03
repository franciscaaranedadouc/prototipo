#Importo utilidades de auth
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django import forms
from django.contrib.auth.models import User
from .forms import UserCreateForm, UserUpdateForm, PerfilForm
import os
import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Mapeo básico de tus categorías al ID de género en IGDB
GENRE_MAP = {
    'accion':    4,
    'aventura': 31,
    'carrera':  10,
    'estrategia': 15,
    'terror':    49,
}

class VideoGameListAPI(APIView):
    """
    GET /api/videogames/?genre=<nombre>
    Devuelve hasta 10 juegos filtrados por género (opcional).
    """
    def get(self, request):
        # 1) Consigue token OAuth de Twitch
        token_res = requests.post(
            'https://id.twitch.tv/oauth2/token',
            data={
                'client_id':     settings.IGDB_CLIENT_ID,
                'client_secret': settings.IGDB_CLIENT_SECRET,
                'grant_type':    'client_credentials'
            }
        )
        if token_res.status_code != 200:
            return Response({'error': 'No se pudo obtener token'}, status=status.HTTP_502_BAD_GATEWAY)

        access_token = token_res.json().get('access_token')

        # 2) Prepara la consulta a IGDB
        hdrs = {
            'Client-ID':     settings.IGDB_CLIENT_ID,
            'Authorization': f'Bearer {access_token}',
        }
        body = 'fields id,name,summary,cover.image_id;'
        genre = request.GET.get('genre')
        if genre:
            gid = GENRE_MAP.get(genre.lower())
            if gid:
                body += f' where genres = ({gid});'
        body += ' limit 10;'

        # 3) Llama a IGDB
        igdb_res = requests.post('https://api.igdb.com/v4/games', headers=hdrs, data=body)
        if igdb_res.status_code != 200:
            return Response(
                {'error': 'Error al consultar IGDB', 'detalle': igdb_res.text},
                status=status.HTTP_502_BAD_GATEWAY
            )

        return Response(igdb_res.json(), status=status.HTTP_200_OK)
    
#Create your views here.
def juegos(request):
    return render(request, 'index.html')

def registro1(request):
    return render(request, 'registro/registrocliente1.html')

def registro2(request):
    return render(request, 'registro/registrocliente2.html')

def registrotrabajador(request):
    return render(request, 'registro/registrotrabajador.html')

def sesion(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('juegos')
        else:
            messages.error(request, "Usuario o contraseña inválidos")
    return render(request, 'registro/iniciosesion.html')

def cerrar_sesion(request):
    request.session.flush()
    return redirect('sesion')

def contraseña(request):
    return render(request, 'registro/contraseña.html')

def categoria_aventura(request):
    return render(request, 'categorias/categoria_aventura.html')

def categoria_accion(request):
    return render(request,'categorias/categoria_accion.html')

def categoria_carrera(request):
    return render(request, 'categorias/categoria_carreras.html')

def categoria_estrategia(request):
    return render(request, 'categorias/categoria_estrategia.html')

def categoria_terror(request):
    return render(request, 'categorias/categoria_terror.html')

def age(request):
    return render(request, 'juegos/age.html')

def eldenring(request):
    return render(request, 'juegos/eldenring.html')

def warhammer(request):
    return render(request, 'juegos/warhammer.html')

def zelda(request):
    return render(request, 'juegos/zelda.html')

def tomb(request):
    return render(request, 'juegos/tomb.html')

def star(request):
    return render(request, 'juegos/star.html')

def outlast(request):
    return render(request, 'juegos/outlast.html')

def resident(request):
    return render(request, 'juegos/resident.html')

def forza(request):
    return render(request, 'juegos/forza.html')

def need(request):
    return render(request, 'juegos/need.html')

def carrito(request):
    return render(request, 'carrito/carrito.html')

def perfil(request):
    return render(request, 'perfil/perfil.html')

def eliminar_perfil(request):
    return render(request, 'perfil/eliminar.html')

@login_required
def perfil_usuario(request):
    usuario = request.user  # Obtiene el usuario autenticado
    return render(request, 'perfil/perfil.html', {'usuario': usuario})  # Renderiza la plantilla perfil.html

@login_required
def editar_perfil(request):
    usuario = request.user
    if request.method == 'POST':
        form = PerfilForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('perfil_usuario')  # Redirige al perfil después de guardar los cambios
    else:
        form = PerfilForm(instance=usuario)
    return render(request, 'perfil/editar.html', {'form': form})

@login_required
def admin_view(request):
    usuario = request.user
    # Verifica si el usuario tiene permisos de administrador
    if not usuario.is_staff:  # Puedes usar `is_staff` o cualquier lógica personalizada
        return redirect('perfil_usuario')  # Redirige a una página si no tiene acceso

    # Renderiza la página de administrador
    return render(request, 'admin.html', {'usuario': usuario})

@login_required
def perfil(request):
    return render(request, 'perfil/perfil.html')
