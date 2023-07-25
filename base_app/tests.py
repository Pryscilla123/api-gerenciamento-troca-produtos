from django.test import TestCase
from django.contrib.auth.models import Group, Permission
from .models import User, GROUP_ADMIN, GROUP_REPOSITOR, GROUP_REPRESENTANTE_DE_LOJA


class UserModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='test123',
                                             cpf='12345678901', telefone='1234567890', nivel_acesso=User.UserRole.REPOSITOR)

    def test_user_creation(self):
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertTrue(self.user.check_password('test123'))
        self.assertEqual(self.user.cpf, '12345678901')
        self.assertEqual(self.user.telefone, '1234567890')
        self.assertEqual(self.user.nivel_acesso, User.UserRole.REPOSITOR)
        self.assertFalse(self.user.aprovado)

    def test_user_group_assignment(self):
        repositor_group = Group.objects.get(name=GROUP_REPOSITOR)
        self.assertTrue(repositor_group in self.user.groups.all())

        admin_group = Group.objects.create(name=GROUP_ADMIN)
        self.user.nivel_acesso = User.UserRole.ADMIN
        self.user.save()
        self.user.refresh_from_db()
        self.assertTrue(admin_group in self.user.groups.all())

    def test_user_signal_receiver(self):
        self.assertEqual(self.user.groups.count(), 1)

        self.user.nivel_acesso = User.UserRole.REPRESENTANTE_DE_LOJA
        self.user.save()
        self.user.refresh_from_db()
        representante_group = Group.objects.get(name=GROUP_REPRESENTANTE_DE_LOJA)
        self.assertTrue(representante_group in self.user.groups.all())

    def test_user_permissions(self):
        permission = Permission.objects.create(codename='can_view_users', name='Can view users', content_type=None)
        self.user.user_permissions.add(permission)
        self.assertEqual(self.user.user_permissions.count(), 1)
        self.assertTrue(permission in self.user.user_permissions.all())


class GroupModelTest(TestCase):

    def test_group_creation(self):
        admin_group = Group.objects.create(name=GROUP_ADMIN)
        repositor_group = Group.objects.create(name=GROUP_REPOSITOR)
        representante_group = Group.objects.create(name=GROUP_REPRESENTANTE_DE_LOJA)

        self.assertEqual(Group.objects.count(), 3)
        self.assertEqual(admin_group.name, GROUP_ADMIN)
        self.assertEqual(repositor_group.name, GROUP_REPOSITOR)
        self.assertEqual(representante_group.name, GROUP_REPRESENTANTE_DE_LOJA)
