from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views 


urlpatterns = [

    path('base/', views.base, name='base'),
    path('index/', views.index, name='index'),
    
    # Autenticación
    path('login_encargado/', views.login_encargado, name='login_encargado'),
    path('login_doctor/', views.login_doctor, name='login_doctor'),
    path('login_paciente/', views.login_paciente, name='login_paciente'),
    path('registro_paciente/', views.registro_paciente, name='registro_paciente'),
    path('logout_paciente', views.logout_paciente, name='logout_paciente'),

    # Dashboards
    path('dashboard_encargado/', views.dashboard_encargado, name='dashboard_encargado'),
    path('dashboard_doctor/', views.dashboard_doctor, name='dashboard_doctor'),
   
    # Gestión de Doctores
    path('doctores_list/', views.doctores_list, name='doctores_list'),
    path('doctores_add/', views.doctores_add, name='doctores_add'),
    path('doctores_edit/<str:pk>/', views.doctores_edit, name='doctores_edit'),  # Cambiado a "id_doctor"
    path('doctores_del/<str:pk>/', views.doctores_del, name='doctores_del'),

    # Otras Vistas
    path('test/', views.test, name='test'),
    path('noticias/', views.noticias, name='noticias'),
    path('noticia/<int:noticia_id>/', views.detalle_noticia, name='detalle_noticia'),
    path('contacto/', views.contacto, name='contacto'),
    path('como_llegar/', views.como_llegar, name='como_llegar'),

    # Horas Médicas
    path('agendar_hora_medica/', views.agendar_hora_medica, name='agendar_hora_medica'),
    path('agendar_hora_dentista/', views.agendar_hora_dentista, name='agendar_hora_dentista'),
    path('citas_paciente/', views.citas_paciente, name='citas_paciente'),
    path('citas_doctor/', views.citas_doctor, name='citas_doctor'),
    path('citas-edit/<int:cita_id>/', views.citas_edit, name='doctor_citas_edit'),
    path('citas/edit_estado/<int:cita_id>/', views.editar_estado_cita, name='doctor_citas_edit_estado'),
    path('eliminar_cita/<int:cita_id>/', views.eliminar_cita, name='eliminar_cita'),
    
    # Exámenes Médicos
    path('examenes/', views.examenes_lista, name='examenes_lista'),
    path('examenes/doctor/', views.examenes_lista_doctor, name='examenes_lista_doctor'),
    path('examenes_crear/', views.examenes_crear, name='examenes_crear'),
    path('examenes-edit<int:pk>/', views.examenes_editar, name='examenes_editar'),
    path('examenes/edit_estado/<int:examen_id>/', views.editar_estado_examen, name='doctor_examenes_edit_estado'),
    path('examenes/eliminar/<int:examen_id>/', views.examenes_eliminar, name='examenes_eliminar'),

    # Recetas Médicas
    path('recetas/<int:examen_id>/', views.recetas_lista, name='recetas_lista'),
    path('recetas/doctor/', views.recetas_lista_doctor, name='recetas_lista_doctor'),
    path('recetas/crear/examen/<int:examen_id>/', views.recetas_crear, name='recetas_crear'),
    path('recetas-edit<int:pk>/', views.recetas_editar, name='recetas_editar'),
    path('recetas/eliminar/<int:pk>/', views.recetas_eliminar, name='recetas_eliminar'),
]


# Solo en modo DEBUG, se sirven archivos estáticos y de medios
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
