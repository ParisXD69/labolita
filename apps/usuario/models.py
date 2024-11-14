from django.template.defaultfilters import title
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
class usuario_manager(BaseUserManager):
    def create_user(self, username, nombre, apellidos, carnet_identidad, password=None):
        usuario = self.model(
            username=username,
            nombre=nombre,
            apellidos=apellidos,
            carnet_identidad=carnet_identidad

        )
        usuario.set_password(password)
        usuario.save()
        return usuario

    def create_superuser(self, username, nombre, apellidos, carnet_identidad, password):
        usuario = self.create_user(
            username=username,
            nombre=nombre,
            apellidos=apellidos,
            carnet_identidad=carnet_identidad,
            password=password
        )
        usuario.usuario_admin = True
        usuario.save()
        return usuario


class usuario(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField('Nombre de usuario', max_length=15, unique=True, blank=False, null=False)
    nombre = models.CharField('Nombre', max_length=15, blank=False, null=False)
    apellidos = models.CharField('Apellidos', null=False, blank=False, max_length=15)
    carnet_identidad = models.DecimalField('Carnet de identidad', max_digits=11,decimal_places=0,blank=False, null=False, unique=True)
    imagen = models.ImageField('Foto de perfil', upload_to='fotos/', blank=True, null=True,default='fotos/user.png')
    privilegios = models.CharField('Privilegios', max_length=20, default='Usuario')
    monto = models.IntegerField('Saldo disponible', default=0)
    activo = models.BooleanField('Estado del usuario', default=False)
    usuario_admin = models.BooleanField('Usuario admin', default=False)
    objects = usuario_manager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['nombre', 'apellidos', 'carnet_identidad']

    def __str__(self):
        return self.nombre + ' ' + self.apellidos

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.usuario_admin


class jugada(models.Model):
    id = models.AutoField('Llave primaria', primary_key=True)
    jugador = models.ForeignKey(usuario, on_delete=models.CASCADE)
    numero_uno = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(75)])
    numero_dos = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(75)])
    numero_tres = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(75)])
    numero_cuatro = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(75)])
    numero_cinco = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(75)])
    numero_seis = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(25)])
    created_at = models.DateField('Fecha de la jugada', auto_now_add=True)
    jugada_activa = models.BooleanField('Jugada activa/no activa', default=True)

    def __str__(self):
        return self.jugador.nombre


class premio_ganador(models.Model):
    premio = models.IntegerField()


class numero_ganador(models.Model):
    id = models.AutoField('Llave primaria', primary_key=True)
    jugador = models.ForeignKey(usuario, on_delete=models.CASCADE)
    numero_uno = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(75)])
    numero_dos = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(75)])
    numero_tres = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(75)])
    numero_cuatro = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(75)])
    numero_cinco = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(75)])
    numero_seis = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(25)])
    fecha_jugada = models.DateField('Fecha de la jugada', auto_now_add=True)
    jugada_activa = models.BooleanField('Jugada activa/no activa', default=True)