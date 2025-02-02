from django.db import models
from django.conf import settings
from django.contrib.auth.models import BaseUserManager, User
from django.utils.timezone import now 




# Modelo Receta
class Receta(models.Model):
    paciente = models.ForeignKey('Paciente', on_delete=models.CASCADE, related_name='recetas')
    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE, related_name='recetas')
    examen = models.ForeignKey('Examen', on_delete=models.CASCADE, related_name='recetas', help_text="Examen relacionado con esta receta (obligatorio).")
    medicamento = models.CharField(max_length=255, verbose_name="Medicamento")
    descripcion = models.TextField(null=True, blank=True, verbose_name="Descripción")
    dosis = models.CharField(max_length=255, null=True, blank=True, verbose_name="Dosis")
    frecuencia = models.CharField(max_length=255, null=True, blank=True, verbose_name="Frecuencia")
    archivo = models.FileField(upload_to='recetas/', null=True, blank=True, help_text="Sube una imagen relacionado con la receta (opcional).")

    def __str__(self):
        return f"Receta: {self.medicamento} - {self.paciente.nombre_completo}"


# Modelo Examen
class Examen(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('realizado', 'Realizado'),
        ('cancelado', 'Cancelado'),
    ]

    nombre_examen = models.CharField(max_length=150, null=True, blank=True, help_text="Nombre opcional del examen (dejar vacío si no aplica).")
    tipo_examen = models.CharField(max_length=100)  # Ejemplo: Laboratorio, Imagenología
    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE, related_name='examenes')
    paciente = models.ForeignKey('Paciente', on_delete=models.CASCADE, related_name='examenes')
    fecha = models.DateTimeField()
    archivo = models.FileField(upload_to='examenes/', null=True, blank=True, help_text="Sube un archivo relacionado con el examen (opcional).")
    estado = models.CharField(max_length=10, choices=ESTADOS, default='pendiente')

    class Meta:
        db_table = 'web_examen'

    def __str__(self):
        return f"{self.tipo_examen} - {self.paciente.nombre_completo if self.paciente else 'Sin asignar'}"


# Modelo Cita
class Cita(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('realizada', 'Realizada'),
        ('cancelada', 'Cancelada'),
        ('pospuesta', 'Pospuesta'),
    ]
    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE, related_name='citas')
    paciente = models.ForeignKey('Paciente', on_delete=models.CASCADE, related_name='citas')
    fecha = models.DateTimeField()
    descripcion = models.TextField()
    estado = models.CharField(max_length=10, choices=ESTADOS, default='pendiente')

    class Meta:
        db_table = 'web_cita'  # Especificar el nombre exacto de la tabla

    def __str__(self):
        return f"Cita de {self.paciente} con {self.doctor} el {self.fecha}"


    
# Modelo Doctor
class Doctor(models.Model):
    id_doctor = models.AutoField(db_column='idDoctor', primary_key=True)
    rut = models.CharField(max_length=12, unique=True, blank=False, null=False)
    contrasena = models.CharField(max_length=128, blank=False, null=False)  # Se puede encriptar con Django
    nombre_completo = models.CharField(max_length=100, blank=False, null=False)
    especialidad = models.CharField(max_length=100, blank=False, null=False)
    telefono = models.CharField(max_length=15, blank=False, null=False)
    imagen = models.ImageField(upload_to="doctores", null=True, blank=True)

    # Campo para registrar la última vez que inició sesión
    last_login = models.DateTimeField(default=now, blank=True, null=True)

    @property
    def is_authenticated(self):
        return True  # Esto indica que siempre está autenticado si está presente

    def __str__(self):
        return str(self.nombre_completo)



# Modelo Paciente Manager
class PacienteManager(BaseUserManager):
    def create_user(self, rut, nombre_completo, password=None):
        if not rut:
            raise ValueError("El RUT es obligatorio")
        
        paciente = self.model(rut=rut, nombre_completo=nombre_completo)
        if password:
            paciente.set_password(password)
        else:
            paciente.set_password("default_password")  # Contraseña predeterminada si no se proporciona
        paciente.save(using=self._db)
        return paciente

    def create_superuser(self, rut, nombre_completo, password):
        paciente = self.create_user(rut, nombre_completo, password)
        paciente.is_staff = True
        paciente.is_superuser = True
        paciente.save(using=self._db)
        return paciente


# Modelo Paciente 
class Paciente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rut = models.CharField(max_length=20)
    nombre_completo = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)  # Nuevo campo para correo electrónico
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre_completo



# Modelo Encargado
class Encargado(models.Model):
    rut = models.CharField(max_length=12, unique=True, null=True, blank=True)
    contrasena = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.rut



# Modelo Noticia
class Noticia(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to="noticias", null=True, blank=True) 
        
    def __str__(self):
        return str(self.titulo)



# Modelo Contacto
class Contacto(models.Model):
    fecha = models.DateField()
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    telefono = models.CharField(max_length=15, blank=True, null=True)
    mensaje = models.TextField()

    def __str__(self):
        return self.nombre