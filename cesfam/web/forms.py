from django import forms
from .models import Contacto, Cita, Examen, Receta
from django.forms.widgets import NumberInput
from django.utils import timezone  # Importar timezone


# Formulario para Recetas Médicas
class RecetaForm(forms.ModelForm):
    class Meta:
        model = Receta
        fields = ['medicamento', 'descripcion', 'dosis', 'frecuencia', 'archivo'] 
        widgets = {
            'medicamento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del medicamento'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción adicional', 'rows': 3}),
            'dosis': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dosis del medicamento'}),
            'frecuencia': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Frecuencia de la medicación'}),
            'archivo': forms.ClearableFileInput(attrs={'class': 'form-control-file', 'required': False}),
        }


# Formulario para Exámenes Médicos
class ExamenForm(forms.ModelForm):
    class Meta:
        model = Examen
        fields = ['nombre_examen', 'tipo_examen', 'doctor', 'paciente', 'fecha', 'archivo', 'estado']
        widgets = {
            'nombre_examen': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el nombre del examen (opcional)'}),
            'tipo_examen': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ejemplo: Laboratorio, Imagenología'}),
            'doctor': forms.Select(attrs={'class': 'form-control'}),
            'paciente': forms.Select(attrs={'class': 'form-control'}),
            'fecha': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'archivo': forms.ClearableFileInput(attrs={'class': 'form-control', 'required': False}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }


# Formulario para Citas Médicas
class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['doctor', 'descripcion', 'fecha']  # Incluimos el campo fecha
    
    # Validación adicional para el campo 'fecha'
    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')
        if fecha < timezone.now():
            raise forms.ValidationError("La fecha debe ser en el futuro.")
        return fecha


# Formulario para Contacto
class ContactoForm(forms.ModelForm):
    fecha = forms.DateField(widget=NumberInput(attrs={'type': 'date'}), label="Fecha")
    nombre = forms.CharField(label="Nombre", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su nombre'}))
    correo = forms.EmailField(label="Correo", widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su correo electrónico'}))
    telefono = forms.CharField(label="Teléfono (Opcional)", required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de teléfono'}))
    mensaje = forms.CharField(label="Mensaje", widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Escriba su mensaje aquí'}))

    class Meta:
        model = Contacto
        fields = ['fecha', 'nombre', 'correo', 'telefono', 'mensaje']
