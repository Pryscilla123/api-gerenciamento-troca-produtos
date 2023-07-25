from django.contrib.auth.models import AbstractUser, UserManager, Group, Permission
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext as _
from django.db import models

# Create your models here.

GROUP_ADMIN = 'admin'
GROUP_REPOSITOR = 'repositor'
GROUP_REPRESENTANTE_DE_LOJA = 'representante_de_loja'


class CustomUserManager(UserManager):
    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_super_user', False)

        return self._create_user(email, email, password, **extra_fields)


class User(AbstractUser):
    class UserRole(models.IntegerChoices):
        REPOSITOR = 1, _('Usuário Repositor')
        ADMIN = 2, _('Usuário Administrador')
        REPRESENTANTE_DE_LOJA = 3, _('Usuário Representante de Loja')
        __empty__ = _('Não definido')

    cpf = models.CharField(null=False, unique=True)
    telefone = models.CharField(null=False)
    nivel_acesso = models.PositiveIntegerField(
        verbose_name=_('nível de acesso'),
        choices=UserRole.choices,
        blank=False,
        default=UserRole.REPOSITOR
    )
    aprovado = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        related_name='custom_users',
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_query_name='custom_user'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        related_name='custom_users',
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_query_name='custom_user'
    )

    objects = CustomUserManager()


@receiver(post_save, sender=User)
def add_created_user_to_group(sender, instance, created, **kwargs):
    instance.groups.clear()
    if instance.nivel_acesso == User.UserRole.ADMIN:
        g, _created = Group.objects.get_or_create(
            name=GROUP_ADMIN)
    if instance.nivel_acesso == User.UserRole.REPOSITOR:
        g, _created = Group.objects.get_or_create(
            name=GROUP_REPOSITOR)
    if instance.nivel_acesso == User.UserRole.REPRESENTANTE_DE_LOJA:
        g, _created = Group.objects.get_or_create(
            name=GROUP_REPRESENTANTE_DE_LOJA)
    instance.groups.add(g)
