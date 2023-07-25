import io

from django.conf import settings
from django.core.mail import send_mail
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from base_app.models import User
from base_app.serializers import UserSerializer, ChangePasswordSerializer, ResetPasswordSerializer


# Create your views here.

class UserViewSets(generics.ListCreateAPIView):

    """
    Rota para cadastro de usuário.

    username -> nome de usuário
    email -> e-mail do usuário
    password -> senha do usuário
    cpf -> CPF do usuário
    telefone -> telefone do usuário
    nivel_acesso -> Nível de acesso do usuário (1 - Repositor, 2 - Administrador, 3 - Representante de loja)
    first_name -> Primeiro nome do usuário
    last_name -> Sobrenome do usuário

    """

    queryset = User.objects.all()
    serializer_class = UserSerializer


def mail(subject, body_text, to_email):
    try:
        send_mail(subject, message=body_text, html_message=body_text,
                  from_email=settings.DEFAULT_FROM_EMAIL,
                  recipient_list=[to_email])

    except Exception as e:
        raise e


SUBJECT_MAIL = "Seu acesso ao Directo"

with io.open('base_app/email_models/forgotten_password.html',
             encoding="utf-8",
             mode='r') as template:
    BODY_TEXT_MAIL = template.read()


def welcome_new_user(full_name, email, password):

    subject = SUBJECT_MAIL
    body_text = BODY_TEXT_MAIL.format(
        full_name=full_name,
        email=email,
        password=password,
    )
    mail(subject, body_text, email)


class ChangePasswordView(generics.UpdateAPIView):

    """
    Routa para pedido de alteração de senha.

    user_cpf -> CPF do usuário cadastrado.

    Após a requisição ser feita um e-mail é enviado ao usuário para que a troca possa ser executada.
    """

    serializer_class = ChangePasswordSerializer
    model = User

    def _get_user(self, serializer_request, queryset=None):
        serializer = self.get_serializer(data=serializer_request.data)

        if serializer.is_valid():
            user = User.objects.get(cpf=serializer.data.get('user_cpf'))
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return user, serializer

    def partial_update(self, request, *args, **kwargs):
        user, serializer = self._get_user(request)

        password = User.objects.make_random_password(length=8)
        welcome_new_user(user.first_name, user.email, password)
        user.set_password(password)
        user.save()

        return Response(status=status.HTTP_200_OK)


class ResetPasswordView(generics.UpdateAPIView):

    """
    Rota para alteração de senha. Essa rota recebe como entrada o código enviado pelo e-mail e a nova senha.

    old_password -> código enviado para o e-mail.
    new_password -> nova senha escolhida pelo usuário.
    """

    serializer_class = ResetPasswordSerializer
    model = User
    permission_classes = [IsAuthenticated]

    def partial_update(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():

            if not user.check_password(serializer.data.get('old_password')):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(serializer.data.get('new_password'))
            user.save()

            return Response({'message': 'Password updated successfully'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
