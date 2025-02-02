from django.contrib.auth.backends import BaseBackend
from .models import Doctor, Paciente
from django.contrib.auth.models import User

class DoctorBackend(BaseBackend):
    def authenticate(self, request, rut=None, contrasena=None):
        try:
            doctor = Doctor.objects.get(rut=rut)
            # Verifica si la contraseña ingresada coincide con la guardada
            if doctor.contrasena == contrasena:  # Si la contraseña no está encriptada
                return doctor
        except Doctor.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Doctor.objects.get(pk=user_id)
        except Doctor.DoesNotExist:
            return None


class PacienteBackend(BaseBackend):
    def authenticate(self, request, rut=None, contrasena=None):
        try:
            # Buscar al usuario por su RUT
            user = User.objects.get(username=rut)
            # Verificar si la contraseña es correcta
            if user.check_password(contrasena):
                # Comprobar si el usuario tiene un paciente asociado
                if hasattr(user, 'paciente'):
                    return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            # Recuperar el usuario por su ID
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

