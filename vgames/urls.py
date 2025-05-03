from django.urls import path, include
from .views import juegos,registro1,registro2,registrotrabajador,sesion,cerrar_sesion,contraseña,perfil,carrito, perfil, VideoGameListAPI
from django.contrib.auth.decorators import login_required
from . import views 
from django.contrib.auth import views as auth_views
from .views import VideoGameListAPI


urlpatterns = [
    path('api/videogames/', VideoGameListAPI.as_view(), name='videogame-list'),
    path('juegos', juegos, name='juegos'),
    path('registro/registro1', registro1, name='registro1'),
    path('registro/registro2', registro2, name='registro2'),
    path('registrotrabajador', registrotrabajador, name='registrotrabajador'),
    path('sesion', sesion, name='sesion'),
    path('logout', cerrar_sesion, name='logout'),
    path('registro/contraseña', contraseña, name='contraseña'),
    path('carrito/carrito', carrito, name='carrito'),
    path('perfil/perfil', perfil, name='perfil'),
    path('perfil/', login_required(views.perfil_usuario), name='perfil_usuario'),
    path('perfil/editar/', login_required(views.editar_perfil), name='editar_perfil'),
    path('perfil/eliminar', login_required(views.eliminar_perfil), name='eliminar_perfil'),
    path('admin/', login_required(views.admin_view), name='admin_view'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    path('perfil/', views.perfil_usuario, name='perfil'),
    path('perfil/registrocliente1.html', registro1, name='registrocliente1'),
    path('perfil/registrocliente2.html', registro2, name='registrocliente2'),
    path('api/videogames/', VideoGameListAPI.as_view(), name='videogame-list'),
]

