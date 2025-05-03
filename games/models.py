from django.db import models

# Create your models here.
from django.db import models

class VideoGame(models.Model):
    name = models.CharField(max_length=100)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
    
class InicioCategoria(models.Model):
    nombre = models.CharField(...)

class InicioProducto(models.Model):
    titulo = models.CharField(...)
    categoria = models.ForeignKey(InicioCategoria, ...)
    # ...
