from rest_framework import viewsets
from .models import Producto
from .serializers import ProductoSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer


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
    