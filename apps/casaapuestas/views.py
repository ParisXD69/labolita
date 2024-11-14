from lib2to3.fixes.fix_input import context
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.db.models import Sum, QuerySet
from django.template.context_processors import request
from django.views.generic import View, CreateView, ListView, UpdateView, DeleteView
from apps.usuario.models import jugada, usuario, premio_ganador
from django.contrib import messages
from apps.usuario.forms import jugada_form, monto_form, premio_form, usuario_form
from django.urls import reverse_lazy
from apps.casaapuestas.models import transaccion
from apps.usuario.models import numero_ganador


# Create your views here.
class crear_usuario(CreateView):
    model = usuario
    template_name = 'register.html'
    success_url = reverse_lazy('login')
    form_class = usuario_form


def index(request):
    context = {}
    context['cant_apuestas'] = jugada.objects.count()
    suma = usuario.objects.aggregate(total=Sum('monto'))
    x = suma['total']
    context['cant_dinero'] = x
    context['apuestas'] = jugada.objects.filter(jugador=request.user.id)
    context['cant_users'] = usuario.objects.count()
    context['numero'] = numero_ganador.objects.all()
    user = usuario.objects.get(id = request.user.id)
    context['monto_user'] = user.monto
    return render(request, 'index.html', context)


def lista_usuarios_activos(request):
    lista = usuario.objects.filter(activo=True, privilegios = 'Usuario')
    queryset = request.GET.get('buscar')
    if queryset:
        lista = usuario.objects.filter(username__icontains = queryset, privilegios = 'Usuario' )
    return render(request, 'usuario/listar_usuario.html', {'lista': lista})


class lista_usuarios_inactivos(ListView):
    model = usuario
    template_name = 'usuario/listar_usuarios_inactivos.html'
    queryset = usuario.objects.filter(activo=False)


class activar(View):
    def get(self, request, pk, *args, **kwargs):
        user = usuario.objects.get(id=pk)
        user.activo = True
        user.save()
        return redirect('listar_usuario_activos')


class listar_jugadas_activas(ListView):
    model = jugada
    template_name = 'apuestas/listar_jugadas_activas.html'
    queryset = jugada.objects.filter(jugada_activa=True)


class listar_jugadas_inactivas(ListView):
    model = jugada
    template_name = 'apuestas/listar_jugadas_activas.html'
    queryset = jugada.objects.filter(jugada_activa=False)


class listar_administradores(ListView):
    model = usuario
    template_name = 'usuario/listar_administradores.html'
    queryset = usuario.objects.filter(privilegios='Administrador')


def crear_apuesta(request):
    form = jugada_form(request.POST or None)
    jugadas_activas = jugada.objects.filter(jugada_activa=True)
    numeros = {}
    u = usuario.objects.get(id=request.user.id)
    if form.is_valid():
        numeros['uno'] = form.cleaned_data['numero_uno']
        numeros['dos'] = form.cleaned_data['numero_dos']
        numeros['tres'] = form.cleaned_data['numero_tres']
        numeros['cuatro'] = form.cleaned_data['numero_cuatro']
        numeros['cinco'] = form.cleaned_data['numero_cinco']
        numeros['seis'] = form.cleaned_data['numero_seis']
        if verificar(jugadas_activas, numeros):
            messages.error(request, 'Esta jugada ya existe')
            return redirect('crear_apuesta')
        if comparador(numeros):
            messages.error(request, 'Los numeros deben estar en orden')
            return redirect('crear_apuesta')
        if comprobar_monto(request) == True:
            messages.error(request, 'No tiene saldo suficiente, Recargue')
            return redirect('crear_apuesta')
        else:
            user = usuario(id=request.user.id, username='x', nombre='x', apellidos='x', carnet_identidad=876798564)
            jugada.objects.create(
                jugador=user,
                numero_uno=form.cleaned_data['numero_uno'],
                numero_dos=form.cleaned_data['numero_dos'],
                numero_tres=form.cleaned_data['numero_tres'],
                numero_cuatro=form.cleaned_data['numero_cuatro'],
                numero_cinco=form.cleaned_data['numero_cinco'],
                numero_seis=form.cleaned_data['numero_seis'],
            )
            saldo = u.monto
            u.monto -= 100
            if u.monto < 100:
                u.monto = saldo
            u.save()

        return redirect('index')

    return render(request, 'apuestas/crear_apuesta.html', {'form': form})


def verificar(x: QuerySet, y: dict):
    devolver = False
    for j in x:
        if j.numero_uno == y['uno'] and j.numero_dos == y['dos'] and j.numero_tres == y['tres'] and j.numero_cuatro == \
                y['cuatro'] and j.numero_cinco == y['cinco'] and j.numero_seis == y['seis']:
            devolver = True
    return devolver


def comparador(x: dict):
    devolver = True
    if (x['uno'] < x['dos'] and x['uno'] < x['tres'] and x['uno'] < x['cuatro'] and x['uno'] < x['cinco']) and (
            x['dos'] < x['tres'] and x['dos'] < x['cuatro'] and x['dos'] < x['cinco']) and (
            x['tres'] < x['cuatro'] and x['tres'] < x['cinco']) and (x['cuatro'] < x['cinco']):
        devolver = False
    print(devolver)
    return devolver


def comprobar_monto(request):
    u = usuario.objects.get(id=request.user.id)
    if u.monto < 100:
        return True


def ingresar(request, id):
    us = usuario.objects.get(id=id)
    form = monto_form(request.POST or None)
    if form.is_valid():
        us.monto += form.cleaned_data['monto']
        us.save()
        transaccion.objects.create(admin=usuario.objects.get(id=request.user.id), usuer=us, tipo='ingreso',
                                   monto=form.cleaned_data['monto'])
        return redirect('listar_usuario_activos')
    return render(request, 'usuario/ingresar_monto.html', {'form': form})


def retirar(request, id):
    us = usuario.objects.get(id=id)
    form = monto_form(request.POST or None)
    if form.is_valid():
        us.monto -= form.cleaned_data['monto']
        us.save()
        transaccion.objects.create(admin=usuario.objects.get(id=request.user.id), usuer=us, tipo='retiro',
                                   monto=form.cleaned_data['monto'])
        return redirect('listar_usuario_activos')
    return render(request, 'usuario/retirar_monto.html', {'form': form})


class ingreso_retiro(ListView):
    queryset = transaccion.objects.order_by('-fecha')
    template_name = 'usuario/ingreso_retiro.html'


class reglas(View):
    template_name = 'apuestas/reglas.html'
    model = premio_ganador

    def get_context_data(self, *args, **kwargs):
        context = {}
        context['lista'] = self.model.objects.all()
        return context

    def get(self, request):
        return render(request, self.template_name, self.get_context_data())


class cambiar_premio(UpdateView):
    model = premio_ganador
    template_name = 'apuestas/cambiar_premio.html'
    form_class = premio_form
    success_url = reverse_lazy('reglas')


class cambiar_numero_ganador(UpdateView):
    model = numero_ganador
    form_class = jugada_form
    template_name = 'apuestas/cambiar_numero_ganador.html'
    success_url = reverse_lazy('index')


def cambiar_password(request):
    if request.method == 'POST':
        username = request.POST.get('usuario')
        carnet = request.POST.get('carnet')
        cont = request.POST.get('password')
        try:
            u = usuario.objects.get(username = username, carnet_identidad = carnet)
            u.password = make_password(cont)
            u.save()
            return redirect('/')
        except :
            messages.error(request, 'El usuario o el numero de carnet no coinciden')

    return render(request,'forget.html')