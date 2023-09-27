from django.urls import path
from . import views

urlpatterns = [
    path('',views.home),
    path('edicionCliente/<codigo>',views.edicionCliente),
    path('bloquearContacto/<codigo>/<cliente>',views.bloquearContacto),
    path('editarCliente/',views.editarCliente),
    path('eliminarContacto/<contacto>/<cliente>',views.eliminarContacto),
    path('gestionContactos/<codigo>',views.gestionContactos),
    path('edicionContacto/<idCliente>/<codigo>/<Gestion>',views.edicionContacto),
    path('gestionDirecciones/<codigo>',views.gestionDirecciones),
    path('edicionClienteDireccion/<idCliente>/<codigo>/<Gestion>',views.edicionClienteDireccion),
    #path('agregarClienteDireccion/<codigo>',views.agregarClienteDireccion),
    path('paises/',views.get_paises),
    path('estados/<codigo>',views.get_estados),
]