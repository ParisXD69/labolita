# Generated by Django 4.2.16 on 2024-11-14 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0012_alter_usuario_carnet_identidad_delete_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='imagen',
            field=models.ImageField(blank=True, default='fotos/user.png', null=True, upload_to='fotos/', verbose_name='Foto de perfil'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='privilegios',
            field=models.CharField(default='Usuario', max_length=10, verbose_name='Privilegios'),
        ),
    ]