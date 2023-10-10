from django.urls import path
from . import views

urlpatterns = [
    #path('',views.home),
    path('',views.login),
    path('home/<usrid>',views.home),
    path('edicionCliente/<codigo>/<usrid>',views.edicionCliente),
    path('editarCliente/<usrid>',views.editarCliente),
    #path('eliminarContacto/<contacto>/<cliente>',views.eliminarContacto),
    path('gestionContactos/<codigo>/<usrid>',views.gestionContactos),
    path('edicionContacto/<idCliente>/<codigo>/<Gestion>/<usrid>',views.edicionContacto),
    path('editarContacto/<usrid>', views.editarContacto),
    path('gestionDirecciones/<codigo>/<usrid>',views.gestionDirecciones),
    path('edicionClienteDireccion/<idCliente>/<codigo>/<Gestion>/<usrid>',views.edicionClienteDireccion),
    path('editarDireccion/<usrid>', views.editarDireccion),
    path('paises/',views.get_paises),
    path('estados/<codigo>',views.get_estados),
    path('codigos/<codigo>',views.get_codigos),
    path('colonias/<codigo>',views.get_colonias),
    path('bloquearContacto/<codigo>/<cliente>/<usrid>',views.bloquearContacto),
    path('bloquearDireccion/<cliente>/<idDireccion>/<usrid>',views.bloquearDireccion),
    path('buscarCliente/<usrid>',views.buscarCliente),
    path('login/',views.login),
    path('cambiarPwd/',views.cambiarPwd),
    path('cambioPwd/',views.cambioPwd),
    path('home_/',views.loginUsr),
]