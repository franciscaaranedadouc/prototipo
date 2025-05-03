# juegosgratis/views.py
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Juego
from .serializers import JuegoSerializer


# Vista API JSON
class JuegosGratisView(APIView):
    def get(self, request):
        juegos = Juego.objects.filter(precio=0)
        serializer = JuegoSerializer(juegos, many=True)
        return Response(serializer.data)

# ✅ Esta función debe estar bien definida (fuera de la clase)
def juegos_list(request):
    juegos = Juego.objects.filter(precio=0)
    return render(request, 'juegosgratis/juegos_list.html', {'juegos': juegos})



