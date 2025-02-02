from django.contrib import admin
from .models import Encargado, Doctor, Paciente, Contacto, Cita, Examen, Receta


class EncargadoAdmin(admin.ModelAdmin):
    # Aquí solo debes poner los campos que realmente existen en el modelo
    list_display = ('rut', 'contrasena')  # Se asume que estos son los campos del modelo
    search_fields = ('rut',)  # Si deseas poder buscar por RUT desde el admin


class PacienteAdmin(admin.ModelAdmin):
    list_display = ('rut', 'nombre_completo', 'correo', 'is_active')  # Mostrar el correo en la lista
    search_fields = ('rut', 'nombre_completo', 'correo')  # Habilitar búsqueda por correo


class ContactoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'correo', 'telefono', 'fecha')  # Muestra estos campos en la lista
    search_fields = ('nombre', 'correo')  # Permite buscar por estos campos
    list_filter = ('fecha',)  # Agrega un filtro por fecha


admin.site.register(Paciente, PacienteAdmin)
admin.site.register(Encargado, EncargadoAdmin)
admin.site.register(Doctor)
admin.site.register(Contacto)
admin.site.register(Cita)
admin.site.register(Examen)
admin.site.register(Receta)
