from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404
from .models import VideoGame
from .serializers import VideoGameSerializer, CategoriaSerializer, JuegoSerializer
from .igdb_client import igdb_request

def lista_juegos(request):
    # Pedimos nombre, portada y género de los 20 más populares
    query = """
      fields id, name, cover.url, genres.name;
      sort popularity desc;
      limit 20;
    """
    juegos = igdb_request('games', query)
    return render(request, 'games/list.html', {'juegos': juegos})

def detalle_juego(request, juego_id):
    query = f"""
      fields name, summary, cover.url, genres.name, first_release_date, platforms.name;
      where id = {juego_id};
    """
    resultado = igdb_request('games', query)
    # asume que devuelve lista con un solo elemento
    juego = resultado[0] if resultado else None
    if not juego:
        # puedes usar Http404
        return render(request, '404.html', status=404)
    return render(request, 'games/detail.html', {'juego': juego})

# Vista para renderizar videojuegos en HTML (opcional)
def videogames_list(request):
    videogames = VideoGame.objects.all()
    return render(request, 'games/videogames_list.html', {'videogames': videogames})

# API basada en clases para retornar videojuegos en JSON
class VideoGameView(APIView):
    def get(self, request):
        videogames = VideoGame.objects.all()
        serializer = VideoGameSerializer(videogames, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = VideoGameSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)