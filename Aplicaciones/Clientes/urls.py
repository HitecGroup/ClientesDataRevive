from django.urls import path
from . import views

urlpatterns = [
    path('',views.home),
    path('edicionCliente/<codigo>',views.edicionCliente),
    path('editarCliente/',views.editarCliente),
    path('eliminarContacto/<contacto>/<cliente>',views.eliminarContacto),
    path('gestionContactos/<codigo>',views.gestionContactos),
    path('edicionContacto/<idCliente>/<codigo>/<Gestion>',views.edicionContacto),
    path('editarContacto/', views.editarContacto),
    path('gestionDirecciones/<codigo>',views.gestionDirecciones),
    path('edicionClienteDireccion/<idCliente>/<codigo>/<Gestion>',views.edicionClienteDireccion),
    path('editarDireccion/', views.editarDireccion),
    path('paises/',views.get_paises),
    path('estados/<codigo>',views.get_estados),
    path('codigos/<codigo>',views.get_codigos),
    path('colonias/<codigo>',views.get_colonias),
    path('bloquearContacto/<codigo>/<cliente>',views.bloquearContacto),
    path('bloquearDireccion/<cliente>/<idDireccion>',views.bloquearDireccion),
    path('buscarCliente/',views.buscarCliente)
]