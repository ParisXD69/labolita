from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(usuario)
admin.site.register(jugada)
admin.site.register(premio_ganador)
admin.site.register(numero_ganador)