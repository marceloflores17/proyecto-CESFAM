from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.utils import timezone

from .models import Encargado, Doctor, Paciente, Noticia, Cita, Examen, Receta
from .forms import ContactoForm, CitaForm, ExamenForm, RecetaForm
from django.contrib.auth.models import User  # Modelo de usuario





#-----------------------------------------------------------------------------------------------------------------
# Index - Base - Test
#-----------------------------------------------------------------------------------------------------------------

def index(request):
    print("hola estoy en index...")
    context ={}
    return render(request, 'web/index.html', context)

def base(request):
    print("hola estoy en base...")
    context ={}
    return render(request, 'web/base.html', context)


def test(request):
    print("hola estoy en test...")
    context ={}
    return render(request, 'web/test.html', context)







#-----------------------------------------------------------------------------------------------------------------
# Registro Paciente - Login - Logout
#-----------------------------------------------------------------------------------------------------------------


def registro_paciente(request):
    if request.method == 'POST':
        rut = request.POST.get("rut")
        contrasena = request.POST.get("contrasena")
        nombre_completo = request.POST.get("nombre_completo")
        correo = request.POST.get("correo")

        # Verificar si el RUT ya está registrado
        if Paciente.objects.filter(rut=rut).exists():
            messages.error(request, "Este RUT ya está registrado. Intente con otro, o inicie sesión.", extra_tags="error")
            return redirect('registro_paciente')

        # Crear un usuario asociado al paciente
        user = User.objects.create_user(username=rut, password=contrasena, email=correo)

        # Crear el paciente y asociarlo al usuario
        Paciente.objects.create(user=user, rut=rut, nombre_completo=nombre_completo, correo=correo)

        # Iniciar sesión automáticamente tras el registro
        user.backend = 'web.backends.PacienteBackend'
        login(request, user)
        return redirect('index')  # Redirigir al index después del registro

    return render(request, 'web/registro_paciente.html')


def login_paciente(request):
    if request.method == "POST":
        rut = request.POST.get("rut")
        contrasena = request.POST.get("contrasena")

        # Autenticar al usuario usando el modelo User
        user = authenticate(request, username=rut, password=contrasena)

        if user is not None:
            try:
                paciente = Paciente.objects.get(user=user)  # Verificar si tiene un perfil de paciente
                login(request, user)  # Iniciar sesión con el usuario
                return redirect("index")  # Redirigir al index
            except Paciente.DoesNotExist:
                messages.error(request, "Este usuario no está registrado como paciente.", extra_tags="error")
                return redirect('login_paciente')  # Regresar al login si no es paciente
        else:
            # Verificar si el RUT existe
            if not User.objects.filter(username=rut).exists():
                messages.error(request, "El RUT no está registrado.", extra_tags="error")
            else:
                messages.error(request, "La contraseña es incorrecta.", extra_tags="error")
            return redirect('login_paciente')  # Regresar al login si la autenticación falla

    return render(request, "web/login_paciente.html")


def logout_paciente(request):
    logout(request)  # Cerrar la sesión del usuario
    return redirect('index')  # Redirigir al índice después de cerrar sesión







#-----------------------------------------------------------------------------------------------------------------
# Login Doctor - Dashboard 
#-----------------------------------------------------------------------------------------------------------------

def login_doctor(request):
    if request.method == 'POST':
        rut = request.POST['rut']
        contrasena = request.POST['contrasena']

        try:
            doctor = Doctor.objects.get(rut=rut)  # Buscar al doctor por su RUT
            if doctor.contrasena == contrasena:  # Verificar la contraseña
                # Guardar la sesión del doctor
                request.session['doctor_id'] = doctor.id_doctor
                return redirect('dashboard_doctor')  # Redirigir al dashboard del doctor
            else:
                # Contraseña incorrecta
                messages.error(request, "La contraseña es incorrecta.")
        except Doctor.DoesNotExist:
            # RUT no registrado
            messages.error(request, "El RUT no está registrado.")

        return render(request, 'web/login_doctor.html')  # Volver al login si hay error

    return render(request, 'web/login_doctor.html')  # Mostrar la página de login inicialmente


def dashboard_doctor(request):
    return render(request, 'web/dashboard_doctor.html')







#-----------------------------------------------------------------------------------------------------------------
# Login Encargado - Dashboard
#-----------------------------------------------------------------------------------------------------------------

def login_encargado(request):
    if request.method == 'POST':
        rut = request.POST.get('rut')  # Obtener RUT del formulario
        contrasena = request.POST.get('contrasena')  # Obtener contraseña del formulario

        try:
            encargado = Encargado.objects.get(rut=rut)  # Buscar al encargado por su RUT
            if encargado.contrasena == contrasena:  # Verificar la contraseña
                # Redirigir al dashboard del encargado
                return redirect('dashboard_encargado')
            else:
                # Contraseña incorrecta
                messages.error(request, "La contraseña es incorrecta.")
        except Encargado.DoesNotExist:
            # RUT no registrado
            messages.error(request, "El RUT no está registrado.")

        return render(request, 'web/login_encargado.html')  # Volver al login si hay error

    return render(request, 'web/login_encargado.html')  # Mostrar la página de login inicialmente


def dashboard_encargado(request):
    return render(request, 'web/dashboard_encargado.html')







#-----------------------------------------------------------------------------------------------------------------
# CRUD Listar - Añadir - Editar - Eliminar Doctores
#-----------------------------------------------------------------------------------------------------------------

def doctores_list(request):
    doctores = Doctor.objects.all()
    context = {'doctores': doctores}
    return render(request, 'web/doctores_list.html', context)

# Agregar nuevo doctor
def doctores_add(request):
    if request.method == "POST":
        rut = request.POST.get('rut')
        contrasena = request.POST.get('contrasena')
        nombre_completo = request.POST.get('nombre_completo')
        especialidad = request.POST.get('especialidad')
        telefono = request.POST.get('telefono')
        imagen = request.FILES.get('imagen')

        # Verificar si el RUT ya existe
        if Doctor.objects.filter(rut=rut).exists():
            messages.error(request, "Ya existe un doctor con este RUT.")
            return render(request, 'web/doctores_add.html', {
                'rut': rut, 
                'nombre_completo': nombre_completo, 
                'especialidad': especialidad, 
                'telefono': telefono, 
                'imagen': imagen
            })

        # Crear el nuevo doctor
        nuevo_doctor = Doctor(
            rut=rut,
            nombre_completo=nombre_completo,
            especialidad=especialidad,
            telefono=telefono,
            imagen=imagen
        )
        contrasena=make_password(contrasena)  # Cifra la contraseña manualmente
        nuevo_doctor.save()
        messages.success(request, "¡Doctor registrado exitosamente!")
        return redirect('doctores_add')  # Redirige a la lista de doctores
    
    return render(request, 'web/doctores_add.html')

# Editar doctor
def doctores_edit(request, pk):
    try:
        doctor = Doctor.objects.get(pk=pk)
        if request.method == "POST":
            rut = request.POST.get('rut')
            contrasena = request.POST.get('contrasena')
            nombre_completo = request.POST.get('nombre_completo')
            especialidad = request.POST.get('especialidad')
            telefono = request.POST.get('telefono')
            imagen = request.FILES.get('imagen')

            # Actualizar los campos del doctor
            doctor.rut = rut
            doctor.contrasena = contrasena
            doctor.nombre_completo = nombre_completo
            doctor.especialidad = especialidad
            doctor.telefono = telefono
            if imagen:
                doctor.imagen = imagen
            doctor.save()

            # Mostrar mensaje de éxito
            messages.success(request, '¡Doctor modificado exitosamente!')
            return redirect('doctores_edit', pk=pk)

        context = {'doctor': doctor}
        return render(request, 'web/doctores_edit.html', context)

    except Doctor.DoesNotExist:
        doctores = Doctor.objects.all()
        context = {'doctores': doctores, 'mensaje': "Error, el doctor no existe..."}
        return render(request, 'web/doctores_list.html', context)


def doctores_del(request, pk):
    try:
        doctor = Doctor.objects.get(pk=pk)
        doctor.delete()
        messages.success(request, "¡Doctor eliminado exitosamente!")  # Mensaje de éxito
        return redirect('doctores_list')  # Redirigir a la lista de doctores después de eliminar

    except Doctor.DoesNotExist:
        messages.error(request, "Error, el doctor no existe...")  # Mensaje de error
        return redirect('doctores_list')  # Redirigir a la lista de doctores en caso de error








#-----------------------------------------------------------------------------------------------------------------
# Noticias - Contacto - Como Llegar
#-----------------------------------------------------------------------------------------------------------------

def noticias(request):
    noticias = Noticia.objects.all()  # Obtén todas las noticias desde la base de datos
    context = {'noticias':noticias}
    return render(request, 'web/noticias.html', context)


def noticias_view(request):
    noticias = Noticia.objects.all()  # Esto obtiene todas las noticias
    context = {'noticias':noticias}
    return render(request, 'web/noticias.html', context)

def detalle_noticia(request, noticia_id):
    noticia = get_object_or_404(Noticia, id=noticia_id)
    context = {'noticia': noticia}  # Usar 'noticia' en lugar de 'noticias'
    return render(request, 'web/detalle_noticia.html', context)


def contacto(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Mensaje enviado con éxito! Nos pondremos en contacto contigo pronto.')
            return redirect('contacto')
        else:
            messages.error(request, 'Hubo un error en el formulario. Por favor, revisa los campos e inténtalo de nuevo.')
    else:
        form = ContactoForm()
    return render(request, 'web/contacto.html', {'form': form})


def como_llegar(request):
    return render(request, 'web/como_llegar.html')







#-----------------------------------------------------------------------------------------------------------------
# Agendar Hora (Medica y Dentista)
#-----------------------------------------------------------------------------------------------------------------

def agendar_hora_medica(request):
    if not request.user.is_authenticated:
        return redirect('login_paciente')
    
    try:
        paciente = request.user.paciente  # Verificar si el usuario tiene un paciente asociado
    except Paciente.DoesNotExist:
        return redirect('login_paciente')
    
    doctores = Doctor.objects.exclude(especialidad="Odontología")
    
    if request.method == 'POST':
        form = CitaForm(request.POST)
        form.instance.paciente = paciente  # Asignar el paciente al formulario
        
        if form.is_valid():
            fecha = form.cleaned_data.get('fecha')
            if fecha < timezone.now():
                messages.error(request, 'La fecha debe ser en el futuro.')
                return redirect('agendar_hora_medica')
            
            form.save()
            messages.success(request, '¡Hora agendada con éxito!')
            return redirect('agendar_hora_medica')
        else:
            messages.error(request, 'La fecha debe ser en el futuro.')
            return redirect('agendar_hora_medica')
    
    form = CitaForm()
    context = {
        'doctores': doctores,
        'form': form
    }
    return render(request, 'web/agendar_hora_medica.html', context)



def agendar_hora_dentista(request):
    if not request.user.is_authenticated:
        return redirect('login_paciente')
    
    try:
        paciente = request.user.paciente  # Verificar si el usuario tiene un paciente asociado
    except Paciente.DoesNotExist:
        return redirect('login_paciente')
    
    doctores = Doctor.objects.filter(especialidad="Odontología")
    
    if request.method == 'POST':
        form = CitaForm(request.POST)
        form.instance.paciente = paciente  # Asignar el paciente al formulario
        
        if form.is_valid():
            fecha = form.cleaned_data.get('fecha')
            if fecha < timezone.now():
                messages.error(request, 'La fecha debe ser en el futuro.')
                return redirect('agendar_hora_dentista')
            
            form.save()
            messages.success(request, '¡Hora agendada con éxito!')
            return redirect('agendar_hora_dentista')
        else:
            messages.error(request, 'La fecha debe ser en el futuro.')
            return redirect('agendar_hora_dentista')
    
    form = CitaForm()
    context = {
        'doctores': doctores,
        'form': form
    }
    return render(request, 'web/agendar_hora_dentista.html', context)







#-----------------------------------------------------------------------------------------------------------------
# Citas (Paciente y Doctor)
#-----------------------------------------------------------------------------------------------------------------


# Citas Paciente - Doctor (Editar)
def citas_paciente(request):
    if request.user.is_authenticated:
        try:
            paciente = Paciente.objects.get(user=request.user)  # Obtener el paciente asociado al usuario autenticado
            citas = Cita.objects.filter(paciente=paciente)  # Obtener solo las citas del paciente autenticado
            return render(request, 'web/citas_paciente.html', {'paciente': paciente, 'citas': citas})
        except Paciente.DoesNotExist:
            return redirect('login_paciente')  # Si el paciente no existe, redirigir al login
    else:
        return redirect('login_paciente')  # Si no está autenticado, redirigir al login


def citas_doctor(request):
    if 'doctor_id' in request.session:
        doctor_id = request.session['doctor_id']
        try:
            doctor = Doctor.objects.get(id_doctor=doctor_id)
            citas = Cita.objects.filter(doctor=doctor)  # Obtener solo las citas del doctor autenticado
            return render(request, 'web/citas_doctor.html', {'doctor': doctor, 'citas': citas})
        except Doctor.DoesNotExist:
            del request.session['doctor_id']
            return redirect('login_doctor')
    else:
        return redirect('login_doctor')


# Editar Cita
def citas_edit(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id)

    if request.method == 'POST':
        nueva_fecha = request.POST.get('fecha')
        try:
            if nueva_fecha:
                cita.fecha = nueva_fecha
                cita.save()
                messages.success(request, "Fecha y hora de la cita actualizada correctamente.")  # Mensaje de éxito
                return redirect('citas_doctor')  # Redirige a citas_doctor
        except Exception as e:
            messages.error(request, f"Error al actualizar la cita: {e}")
            return redirect('citas_doctor')  # Redirige de vuelta a la lista de citas en caso de error

    return redirect('citas_doctor')  # En caso de un método no permitido, también redirige a la página de citas


# Editar Estado Cita
def editar_estado_cita(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id)

    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        if nuevo_estado:
            cita.estado = nuevo_estado
            cita.save()
            messages.success(request, "Estado de la cita actualizado correctamente.")
        return redirect('citas_doctor')

    return redirect('citas_doctor')


# Eliminar Cita
def eliminar_cita(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id)
    cita.delete()
    return redirect('citas_doctor')






#-----------------------------------------------------------------------------------------------------------------
# Examenes (Paciente y Doctor)
#-----------------------------------------------------------------------------------------------------------------

# Exámenes Médicos
def examenes_lista(request):
    if not request.user.is_authenticated:
        return redirect('login_paciente')
    
    try:
        paciente = request.user.paciente  # Verificar si el usuario tiene un paciente asociado
    except Paciente.DoesNotExist:
        return redirect('login_paciente')
    
    examenes = Examen.objects.filter(paciente=paciente)
    return render(request, 'web/examenes_lista.html', {'examenes': examenes})


def examenes_lista_doctor(request):
    if 'doctor_id' in request.session:
        doctor_id = request.session['doctor_id']
        try:
            # Obtiene al doctor a partir del id almacenado en la sesión
            doctor = Doctor.objects.get(id_doctor=doctor_id)
            # Filtra los exámenes para mostrar solo los del doctor autenticado
            examenes = Examen.objects.filter(doctor=doctor)
            
            # Añadimos el campo receta_existente a cada examen
            for examen in examenes:
                receta_existente = Receta.objects.filter(examen=examen).first()
                examen.receta_existente = receta_existente  # Asignamos receta_existente al examen
            
            return render(request, 'web/examenes_lista_doctor.html', {
                'doctor': doctor,
                'examenes': examenes
            })
        except Doctor.DoesNotExist:
            # Si no se encuentra al doctor, eliminamos su id de la sesión y lo redirigimos al login
            del request.session['doctor_id']
            return redirect('login_doctor')
    else:
        # Si no hay id de doctor en la sesión, redirigimos al login
        return redirect('login_doctor')


# Crear Examen
def examenes_crear(request):
    doctores = Doctor.objects.all()
    pacientes = Paciente.objects.all()

    # Obtener el doctor autenticado usando el ID almacenado en la sesión
    try:
        doctor = Doctor.objects.get(id_doctor=request.session['doctor_id'])
    except Doctor.DoesNotExist:
        messages.error(request, "Hubo un problema con tu sesión. Por favor, inicia sesión nuevamente.")
        return redirect('doctor_login')

    # Obtener solo los pacientes activos
    pacientes = Paciente.objects.filter(is_active=True)

    if request.method == 'POST':
        form = ExamenForm(request.POST, request.FILES)
        if form.is_valid():
            # Crear el examen y asociarlo con el doctor autenticado
            examen = form.save(commit=False)
            examen.doctor = doctor
            examen.save()
            messages.success(request, "Examen creado exitosamente.")
            return redirect('examenes_lista_doctor')  # Redirige a la lista de exámenes
        else:
            print(form.errors)  # Esto imprimirá los errores de validación en la consola
            messages.error(request, "Por favor, corrige los errores en el formulario.")
    else:
        form = ExamenForm()

    # Renderizar el formulario de creación de exámenes
    return render(request, 'web/examenes_crear.html', {
        'form': form,
        'doctores': doctores,
        'pacientes': pacientes,
    })


# Editar Examen
def examenes_editar(request, pk):
    examen = get_object_or_404(Examen, pk=pk)
    archivo_tipo = None

    # Verificar tipo de archivo
    if examen.archivo:
        archivo_name = examen.archivo.name.lower()
        if archivo_name.endswith(('.jpg', '.jpeg', '.png', '.jfif')):
            archivo_tipo = 'imagen'
        elif archivo_name.endswith('.pdf'):
            archivo_tipo = 'pdf'
        else:
            archivo_tipo = 'otro'

    if request.method == 'POST':
        form = ExamenForm(request.POST, request.FILES, instance=examen)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "El examen ha sido actualizado correctamente.")
                return redirect('examenes_editar', pk=examen.pk)
            except Exception as e:
                messages.error(request, f"Error al actualizar el examen: {e}")
        else:
            messages.error(request, "Por favor corrige los errores en el formulario.")
    else:
        form = ExamenForm(instance=examen)

    return render(request, 'web/examenes_editar.html', {
        'form': form,
        'examen': examen,
        'archivo_tipo': archivo_tipo
    })


# Editar Estado Examen
def editar_estado_examen(request, examen_id):

    examen = get_object_or_404(Examen, pk=examen_id)

    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')  # Asegúrate de tener un input llamado "estado" en tu formulario
        if nuevo_estado:
            try:
                examen.estado = nuevo_estado
                examen.save()
                messages.success(request, "El estado del examen ha sido actualizado correctamente.")
            except Exception as e:
                messages.error(request, f"Hubo un error al actualizar el estado del examen: {e}")

        return redirect('examenes_lista_doctor')  # Cambia esto si usas otra URL para la lista

    return redirect('examenes_lista_doctor')  # Método no permitido, redirige a la lista


# Eliminar Examen
def examenes_eliminar(request, examen_id):
    examen = get_object_or_404(Examen, id=examen_id)

    if request.method == 'POST':
        examen.delete()
        messages.success(request, "Examen eliminado correctamente.")
        return redirect('examenes_lista_doctor')  # Redirige a la lista de exámenes

    return render(request, 'web/examenes_eliminar.html', {'examen': examen})







#-----------------------------------------------------------------------------------------------------------------
# Recetas (Paciente y Doctor)
#-----------------------------------------------------------------------------------------------------------------

# Lista de Recetas para Pacientes
def recetas_lista(request, examen_id):
    if not request.user.is_authenticated:
        return redirect('login_paciente')
    
    try:
        paciente = request.user.paciente  # Verificar si el usuario tiene un paciente asociado
    except Paciente.DoesNotExist:
        return redirect('login_paciente')

    examen = get_object_or_404(Examen, id=examen_id, paciente=paciente)
    receta = Receta.objects.filter(paciente=paciente, examen=examen).first()  # Solo la receta de ese examen

    return render(request, 'web/recetas_lista.html', {'receta': receta, 'examen': examen})


# Lista de Recetas para Doctores
def recetas_lista_doctor(request):
    if 'doctor_id' in request.session:
        doctor_id = request.session['doctor_id']
        try:
            # Obtiene al doctor a partir del id almacenado en la sesión
            doctor = Doctor.objects.get(id_doctor=doctor_id)
            # Filtra las recetas para mostrar solo las del doctor autenticado
            recetas = Receta.objects.filter(doctor=doctor)
            return render(request, 'web/recetas_lista_doctor.html', {'doctor': doctor, 'recetas': recetas})
        except Doctor.DoesNotExist:
            # Si no se encuentra al doctor, eliminamos su id de la sesión y lo redirigimos al login
            del request.session['doctor_id']
            return redirect('login_doctor')
    else:
        # Si no hay id de doctor en la sesión, redirigimos al login
        return redirect('login_doctor')


# Crear Receta
def recetas_crear(request, examen_id):
    if 'doctor_id' not in request.session:
        return redirect('login_doctor')

    examen = get_object_or_404(Examen, id=examen_id)
    doctor = get_object_or_404(Doctor, id_doctor=request.session['doctor_id'])
    paciente = examen.paciente

    receta_existente = Receta.objects.filter(examen=examen).first()
    if receta_existente:
        return redirect('recetas_editar', pk=receta_existente.id)

    if request.method == 'POST':
        form = RecetaForm(request.POST, request.FILES)
        if form.is_valid():
            receta = form.save(commit=False)
            receta.examen = examen
            receta.doctor = doctor
            receta.paciente = paciente
            receta.save()
            messages.success(request, "Receta creada exitosamente.")
            return redirect('examenes_lista_doctor')
        else:
            messages.error(request, f"Error al guardar la receta: {form.errors}")
    else:
        form = RecetaForm()

    return render(request, 'web/recetas_crear.html', {
        'form': form,
        'examen': examen
    })


# Editar Receta
def recetas_editar(request, pk):
    if 'doctor_id' not in request.session:
        return redirect('login_doctor')

    receta = get_object_or_404(Receta, pk=pk)
    doctor = get_object_or_404(Doctor, id_doctor=request.session['doctor_id'])

    if receta.doctor != doctor:
        messages.error(request, "No puedes editar esta receta.")
        return redirect('recetas_lista_doctor')

    if request.method == 'POST':
        form = RecetaForm(request.POST, request.FILES, instance=receta)
        if form.is_valid():
            form.save()
            messages.success(request, "Receta actualizada exitosamente.")
            return redirect('examenes_lista_doctor')
        else:
            messages.error(request, f"Error al actualizar la receta: {form.errors}")
    else:
        form = RecetaForm(instance=receta)

    return render(request, 'web/recetas_editar.html', {
        'form': form,
        'receta': receta
    })


# Eliminar Receta
def recetas_eliminar(request, pk):
    receta = get_object_or_404(Receta, pk=pk)

    if request.method == 'POST':
        receta.delete()
        messages.success(request, "Receta eliminada correctamente.")
        return redirect('examenes_lista_doctor')  # Redirige correctamente

    return render(request, 'web/recetas_eliminar.html', {'receta': receta})

