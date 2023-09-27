from django.http import JsonResponse
from django.shortcuts import redirect, render
from . models import Clientes
from . models import Contactos
from .models import Direcciones

# Create your views here.
def home(request):
    clientes = Clientes.objects.all()
    return render(request, "gestionClientes.html",{"clientes":clientes})

def edicionCliente(request,codigo):
    cliente = Clientes.objects.get(IdCliente=codigo)
    return render(request, "edicionCliente.html",{"cliente":cliente})

def editarCliente(request):
    IdCliente = request.POST['claveExterna']
    NombreCliente = request.POST['nombreCliente']
    TipoCliente = request.POST['tipoCliente']
    ClientePotencial = request.POST['clientePotencial']
    FechaNacimiento = request.POST['fechaNacimiento']
    tier = request.POST['tier']
    tipoCliente = request.POST['tipoCliente']
    clientePotencial = request.POST['clientePotencial']
    duns = request.POST['DUNS']
    sector = request.POST['Sector']
    clasificacionCliente = request.POST['clasificacionCliente']
    division = request.POST['division']
    zonaServicio = request.POST['zonaServicio']
    tipoEmpresa = request.POST['tipoEmpresa']
    noTurnos = request.POST['noTurnos']
    NoMaqConve = request.POST['NoMaqConve']
    NoMaqCNC = request.POST['NoMaqCNC']
    division = request.POST['division']
    subdivision = request.POST['subDivision']


    cliente = Clientes.objects.get(IdCliente=IdCliente)
    cliente.NombreCliente = NombreCliente
    cliente.TipoCliente = TipoCliente
    cliente.ClientePotencial = ClientePotencial
    cliente.FechaNacimiento = FechaNacimiento
    cliente.Tier = tier
    cliente.TipoCliente = tipoCliente
    cliente.ClientePotencial = clientePotencial
    cliente.Duns = duns
    cliente.Sector = sector
    cliente.Clasificacion = clasificacionCliente
    cliente.Division = division
    cliente.SucServicio = zonaServicio
    cliente.TipoEmpresa = tipoEmpresa
    cliente.NoTurnosC = noTurnos
    cliente.NoMaqConvenC = NoMaqConve
    cliente.NoMaqCNC_C = NoMaqCNC
    cliente.Division = division
    cliente.subDivision = subdivision
    cliente.save()

    return redirect('/')

def gestionContactos(request,codigo):
    cliente = Clientes.objects.get(IdCliente=codigo)
    if Contactos.objects.filter(IdCliente=codigo).exists():
        contactosListados = Contactos.objects.all().filter(IdCliente=codigo)
    # Si el cliente tiene contactos envía el listado de contactos del cliente
        return render(request,"gestionContactos.html",{"contactos":contactosListados, "cliente":cliente})
    else:
    # Si no hay contactos registrados, se envía agregar un contacto
        return render(request, "edicionContactos.html",{"Gestion":False, "idContacto":0, "contacto":None, "cliente":cliente, "variable":True})

def edicionContacto(request, idCliente, codigo, Gestion):
        
    cliente = Clientes.objects.get(IdCliente=idCliente)
    if codigo=="0" :
        contacto = None
    else :
        contacto = Contactos.objects.get(IdContacto=codigo)
        
    return render(request, "edicionContactos.html",{"Gestion":Gestion, "idContacto":codigo, "contacto":contacto, "cliente":cliente, "variable":True})

def editarContacto(request):
    IdCliente = request.POST['claveExterna']
    NombreContacto = request.POST['nombreContacto']
    ClaveExterna = request.POST['cvexterna']

    contacto = Contactos.objects.get(IdCliente=IdCliente)
    contacto.NombreContacto = NombreContacto
    contacto.ClaveExterna = ClaveExterna
    contacto.save()

    return redirect('/')

def eliminarContacto(request,contacto,cliente):
    contacto = Contactos.objects.get(IdContacto=contacto)
    contacto.delete()
    contactosListados = Contactos.objects.all().filter(IdCliente=cliente)
    return render(request,"gestionContactos.html",{"contactos":contactosListados})

def gestionDirecciones(request,codigo):    
    cliente = Clientes.objects.get(IdCliente=codigo)
    listPais = ['País1', 'País2','País3']
    if Direcciones.objects.filter(IdCliente=codigo).exists():
        direccionesListados = Direcciones.objects.all().filter(IdCliente=codigo)
    # Si hay direcciones, se envía a gestión de direcciones
        return render(request,"gestionDirecciones.html",{"direcciones":direccionesListados, "cliente":cliente})
    else:
    # Si no hay direcciones registradas, se envía a agregar una dirección
        return render(request,"edicionClienteDireccion.html",{"Gestion":False, "id":0, "cliente":cliente, "listPaises":listPais})
    
def edicionClienteDireccion(request,idCliente, codigo, Gestion):
    cliente = Clientes.objects.get(IdCliente=idCliente)
    listPais = ['País1', 'País2','País3']
    if codigo=="0" :
        direcciones = None
    else :
        direcciones = Direcciones.objects.get(IdCliente=codigo)
        
    return render(request, "edicionClienteDireccion.html",{"Gestion": Gestion, "id":codigo, "direcciones":direcciones, "cliente":cliente, "listPaises":listPais})

#def agregarClienteDireccion(request,codigo):
#    return render(request,"agregarClienteDireccion.html",{"cliente":codigo})

    
def get_paises(request):
    paises = list(Clientes.objects.values())
    if (len(paises)>0):
        data={'message':"Success", 'paises':paises}
    else:
        data={"message":"Not Found"}

    return JsonResponse(data)

def get_estados(request, codigo):
    estados = list(Contactos.objects.filter(IdCliente=codigo).values())
    if (len(estados)>0):
        data={'message':"Success", 'estados':estados}
    else:
        data={"message":"Not Found"}

    return JsonResponse(data)

def bloquearContacto(request, codigo,cliente):
    contacto = Contactos.objects.get(IdContacto=codigo)
    contacto.Bloqueo = True
    contacto.save()

    contactosListados = Contactos.objects.all().filter(IdCliente=cliente)

    return render(request,"gestionContactos.html",{"contactos":contactosListados, "cliente":cliente})


