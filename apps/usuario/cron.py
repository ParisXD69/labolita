from django_cron import CronJobBase, Schedule
from django.utils import timezone
from datetime import timedelta
from .models import jugada  # Cambia esto por tu modelo

class EliminarObjetosAntiguosCronJob(CronJobBase):
    RUN_EVERY_MINS = 60  # Cambia esto a la frecuencia deseada

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'usuario.eliminar_objetos_antiguos'  # Un código único para la tarea

    def do(self):
        tiempo_limite = timezone.now() - timedelta(days=3)  # Ajusta el tiempo según sea necesario
        jugada.objects.filter(fecha_jugada = tiempo_limite).delete()