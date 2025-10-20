from django.apps import AppConfig


class UsuariosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'usuarios'

    def ready(self):
        # registro do handler aqui (import local)
        from django.db.models.signals import post_migrate
        from django.contrib.auth.models import Group, Permission
        from django.apps import apps
        def criar_grupos(sender, **kwargs):
            # cria o grupo "professores" e associa a permissão custom
            Group = apps.get_model('auth', 'Group')
            Permission = apps.get_model('auth', 'Permission')
            grupo, created = Group.objects.get_or_create(name='professores')
            try:
                perm = Permission.objects.get(codename='acessar_area_professor', content_type__app_label='usuarios')
                grupo.permissions.add(perm)
            except Permission.DoesNotExist:
                # permissão ainda não criada (ou migração não aplicada) — nada a fazer agora
                pass

        post_migrate.connect(criar_grupos, sender=self)
