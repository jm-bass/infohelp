from django.db import models
from django.contrib.auth.models import AbstractUser

# 2 linhas abaixo utilizadas na criação do perfil do superadmin por terminal
from django.db.models.signals import post_save
from django.dispatch import receiver

class User(AbstractUser):
    def __str__(self):
        return self.username
    
class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    cidade = models.CharField(max_length=50, null=True)
    estado = models.CharField(max_length=50, null=True)
    data_nascimento = models.DateField(null=True)
    telefone = models.CharField(max_length=20, null=True)
    avatar = models.ImageField(null=True, blank=True)
    solicitacao_professor = models.BooleanField(default=False)  # Novo campo

    def __str__(self):
        return self.usuario.username

    class Meta:
        permissions = [
            ("acessar_area_professor", "Pode acessar a área de professor"),
        ]

@receiver(post_save, sender=User)
def criar_perfil_para_superuser(sender, instance, created, **kwargs):
    """
    Ao criar um superuser (via createsuperuser ou outro lugar),
    garante a criação do Perfil relacionado (campo 'usuario').
    """
    if created and getattr(instance, "is_superuser", False):
        Perfil.objects.get_or_create(usuario=instance)