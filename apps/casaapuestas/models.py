from django.db import models
from apps.usuario.models import usuario
# Create your models here.

class transaccion(models.Model):
    admin = models.ForeignKey(usuario, on_delete=models.CASCADE, related_name='admin')
    usuer = models.ForeignKey(usuario, on_delete=models.CASCADE, related_name='user')
    tipo = models.CharField(max_length=10,null=True,blank=True)
    monto = models.IntegerField('Monto',default=0)
    fecha = models.DateField('Fecha', auto_now=True)
