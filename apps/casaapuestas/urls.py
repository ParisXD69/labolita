from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.staticfiles.urls import static

urlpatterns = [
                  path('', login_required(index), name='index'),
                  path('listar_usuario_activos/', login_required(lista_usuarios_activos),
                       name='listar_usuario_activos'),
                  path('listar_usuario_inactivos/', login_required(lista_usuarios_inactivos.as_view()),
                       name='listar_usuario_inactivos'),
                  path('activar_usuario/<int:pk>', login_required(activar.as_view()), name='activar'),
                  path('listar_jugadas_activas/', login_required(listar_jugadas_activas.as_view()),
                       name='listar_jugadas_activas'),
                  path('listar_jugadas_inactivas/', login_required(listar_jugadas_inactivas.as_view()),
                       name='listar_jugadas_inactivas'),
                  path('listar_administradores/', login_required(listar_administradores.as_view()),
                       name='listar_administradores'),
                  path('crear_apuesta/', login_required(crear_apuesta), name='crear_apuesta'),
                  path('ingresar/<id>', login_required(ingresar), name='ingresar'),
                  path('reglas/', login_required(reglas.as_view()), name='reglas'),
                  path('cambiar_premio/<int:pk>', login_required(cambiar_premio.as_view()), name='cambiar_premio'),
                  path('retirar/<id>', login_required(retirar), name='retirar'),
                  path('ingreso_retiro/', login_required(ingreso_retiro.as_view()), name='ingreso_retiro'),
                  path('cambiar_numero/<int:pk>', login_required(cambiar_numero_ganador.as_view()),
                       name='cambiar_numero'),
                  path('crear_usuario/', crear_usuario.as_view(), name='crear_usuario'),
                  path('cambiar_pass/',cambiar_password,name='cambiar_pass')

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
