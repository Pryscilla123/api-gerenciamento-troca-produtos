from rest_framework.permissions import BasePermission

from base_app.models import GROUP_REPOSITOR, GROUP_ADMIN, GROUP_REPRESENTANTE_DE_LOJA


class IsRepositorGroupPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name__in=[GROUP_REPOSITOR]).exists() and request.user.aprovado


class IsAdminGroupPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name__in=[GROUP_ADMIN]).exists() and request.user.aprovado


class IsRepresentanteDeLojaGroupPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name__in=[GROUP_REPRESENTANTE_DE_LOJA]).exists() and request.user.aprovado
