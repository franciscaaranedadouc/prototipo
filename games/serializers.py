from rest_framework import serializers
from .models import VideoGame
from games.models import InicioCategoria, InicioProducto
from .serializers import CategoriaSerializer, JuegoSerializer
from Inicio.models import InicioCategoria, InicioProducto

class VideoGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoGame
        fields = '__all__'

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = InicioCategoria
        fields = ['id', 'nombre']

class JuegoSerializer(serializers.ModelSerializer):
    class Meta:
        model = InicioProducto
        fields = ['id', 'titulo', 'descripcion', 'url', 'categoria']

class CategoriaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = InicioCategoria.objects.all()
    serializer_class = CategoriaSerializer

class JuegoViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = JuegoSerializer

    def get_queryset(self):
        cat_id = self.request.query_params.get('categoria')
        if cat_id:
            return InicioProducto.objects.filter(categoria_id=cat_id)
        return InicioProducto.objects.all()