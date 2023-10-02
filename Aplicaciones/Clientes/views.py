from django.http import JsonResponse
from django.shortcuts import redirect, render
from . models import Clientes
from . models import Contactos
from .models import Direcciones
from .models import Country
from .models import Region
from .models import RelReg_Edo
from .models import Sepomex
from django.db.models.aggregates import Count
from django.db.models.aggregates import Sum

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
        contacto = None
        flag1 = flag2 =False
        iniCodPos = ""
        iniDistrito = ""
        iniPais = {"CodeId":"MX", "Descrip":"México"}
        iniRegion = {"CodeId":"CMX", "Descrip":"Ciudad de México"}
        iniCheckbox = {"Principal":flag1, "VIP":flag2}
        return render(request, "edicionContactos.html",{"vista":"Contacto", "Gestion":False, "idContacto":codigo, "contacto":contacto, "cliente":cliente, "iniPais":iniPais, "iniRegion":iniRegion, "iniCodPos":iniCodPos, "iniDistrito":iniDistrito, "dataInt":False, "iniCheckbox":iniCheckbox })

def edicionContacto(request, idCliente, codigo, Gestion):        
    cliente = Clientes.objects.get(IdCliente=idCliente)
    iniCodPos = ""
    iniDistrito = ""
    dataInt = False
    flag1 = flag2 =False
    if codigo=="0" :
        contacto = None
        iniPais = {"CodeId":"MX", "Descrip":"México"}
        iniRegion = {"CodeId":"CMX", "Descrip":"Ciudad de México"}
    else :
        contacto = Contactos.objects.get(IdContacto=codigo)
        idPais = contacto.PaisRegion
        pais = region = None
        pdescrip = rdescrip = ""
        if Country.objects.filter(CodeId=contacto.PaisRegion).exists():
            pais = Country.objects.get(CodeId=contacto.PaisRegion)
            pdescrip = pais.Descrip
            
            if Region.objects.filter(IdCountry=idPais, CodeId=contacto.Estado).exists():
                region = Region.objects.get(IdCountry=idPais, CodeId=contacto.Estado)
                rdescrip = region.Descrip

        iniCodPos = contacto.CodigoPostal
        iniDistrito = contacto.Distrito

        if(idPais!='MX'):
            dataInt = True
        iniPais = {"CodeId":idPais, "Descrip":pdescrip}
        iniRegion = {"CodeId":contacto.Estado, "Descrip":rdescrip}

        if(contacto.Principal!=""):
            flag1 = True
        if(contacto.Vip!=""):
            flag2 = True

    iniCheckbox = {"Principal":flag1, "VIP":flag2}
    
    return render(request, "edicionContactos.html",{"vista":"Contacto", "Gestion":Gestion, "idContacto":codigo, "contacto":contacto, "cliente":cliente, "iniPais":iniPais, "iniRegion":iniRegion, "iniCodPos":iniCodPos, "iniDistrito":iniDistrito, "dataInt":dataInt, "iniCheckbox":iniCheckbox })

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
    if Direcciones.objects.filter(IdCliente=codigo).exists():
        direccionesListados = Direcciones.objects.all().filter(IdCliente=codigo)
    # Si hay direcciones, se envía a gestión de direcciones
        return render(request,"gestionDirecciones.html",{"direcciones":direccionesListados, "cliente":cliente})
    else:
    # Si no hay direcciones registradas, se envía a edicionClienteDireccion
        flag1 = flag2 = flag3 = flag4 = False
        iniCodPos = ""
        iniDistrito = ""
        iniPais = {"CodeId":"MX", "Descrip":"México"}
        iniRegion = {"CodeId":"CMX", "Descrip":"Ciudad de México"}
        iniCodDomFis = {"CodeId":"US", "Descrip":"Alabama"}
        iniCheckbox = {"DireccionPrincipal":flag1, "Entrega":flag2, "DestinatarioMercEstandar":flag3, "DestinatarioFactura":flag4}    
        
        return render(request,"edicionClienteDireccion.html",{"vista":"Cliente", "Gestion":False, "id":0, "cliente":cliente, "iniPais":iniPais, "iniRegion":iniRegion, "iniCodPos":iniCodPos, "iniCodDomFis":iniCodDomFis, "iniDistrito":iniDistrito, "dataInt":False, "dataUS":False, "iniCheckbox":iniCheckbox})
    
def edicionClienteDireccion(request,idCliente, codigo, Gestion):
    cliente = Clientes.objects.get(IdCliente=idCliente)
    iniCodPos = ""
    iniDistrito = ""
    coddomfis=""
    dataInt = False
    dataUS = False
    flag1 = flag2 = flag3 = flag4 = False

    if codigo=="0" :
        direcciones = None
        iniPais = {"CodeId":"MX", "Descrip":"México"}
        iniRegion = {"CodeId":"CMX", "Descrip":"Ciudad de México"}
        iniCodDomFis = {"CodeId":"US", "Descrip":"Alabama"}        
    else :
        direcciones = Direcciones.objects.get(IdRegistro=codigo)
        idPais = direcciones.PaisRegion
        pais = region = None
        pdescrip = rdescrip = ""
        if Country.objects.filter(CodeId=direcciones.PaisRegion).exists():
            pais = Country.objects.get(CodeId=direcciones.PaisRegion)
            pdescrip = pais.Descrip
            
            if Region.objects.filter(IdCountry=idPais, CodeId=direcciones.Estado).exists():
                region = Region.objects.get(IdCountry=idPais, CodeId=direcciones.Estado)
                rdescrip = region.Descrip        
                
        iniCodPos = direcciones.CodigoPostal
        iniDistrito = direcciones.Distrito
        if(idPais!='MX'):
            dataInt = True
            if(idPais=='US'):
                dataUS = True
                coddomfis = ""
                if(direcciones.CodigoDomFiscal != ""):
                    regcoddomfis = Region.objects.get(IdCountry=idPais, CodeId=direcciones.CodigoDomFiscal)
                    coddomfis=regcoddomfis.Descrip

        iniPais = {"CodeId":idPais, "Descrip":pdescrip}
        iniRegion = {"CodeId":direcciones.Estado, "Descrip":rdescrip}
        iniCodDomFis = {"CodeId":direcciones.CodigoDomFiscal, "Descrip":coddomfis}

        if(direcciones.DireccionPrincipal!=""):
            flag1 = True
        if(direcciones.Entrega!=""):
            flag2 = True
        if(direcciones.DestinatarioMercEstandar!=""):
            flag3 = True
        if(direcciones.DestinatarioFactura!=""):
            flag4 = True

    iniCheckbox = {"DireccionPrincipal":flag1, "Entrega":flag2, "DestinatarioMercEstandar":flag3, "DestinatarioFactura":flag4}
    return render(request, "edicionClienteDireccion.html",{"vista":"Cliente", "Gestion": Gestion, "id":codigo, "direcciones":direcciones, "cliente":cliente, "iniPais":iniPais, "iniRegion":iniRegion, "iniCodPos":iniCodPos, "iniCodDomFis":iniCodDomFis, "iniDistrito":iniDistrito, "dataInt":dataInt, "dataUS":dataUS, "iniCheckbox":iniCheckbox})

def editarDireccion(request):
    idRegistro = request.POST['idRegistro']
    IdCliente = request.POST['idCliente']
    PaisRegion = request.POST['PaisRegion']
    Calle = request.POST['Calle']
    Numero = request.POST['Numero']
    Calle2 = request.POST['Calle2']
    Ciudad = request.POST['Ciudad']
    Estado = request.POST['Estado']
    CodigoPostal = request.POST['CodigoPostal']
    Distrito = request.POST['Distrito']
    CodigoDomFiscal = ""
    Telefono = request.POST['Telefono']
    CorreoElectronico = request.POST['CorreoElectronico']
    SitioWeb = request.POST['SitioWeb']   

    if(PaisRegion=="US"):
        CodigoDomFiscal = request.POST['CodigoDomFiscal']
    
    DireccionPrincipal = Entrega = ""
    DestinatarioMercEstandar = DestinatarioFactura = ""

    if "DireccionPrincipal" in request.POST:
        DireccionPrincipal = "X"    
    if 'Entrega' in request.POST:
        Entrega = "X"
    if "DestinatarioMercEstandar" in request.POST:
        DestinatarioMercEstandar = "X"
    if 'DestinatarioFactura' in request.POST:
        DestinatarioFactura = "X"

    if(idRegistro!="0"):
        direcciones = Direcciones.objects.get(IdRegistro=idRegistro)
        direcciones.IdCliente = IdCliente
        direcciones.PaisRegion = PaisRegion
        direcciones.Calle = Calle
        direcciones.Numero = Numero
        direcciones.Calle2 = Calle2
        direcciones.Ciudad = Ciudad
        direcciones.Estado = Estado
        direcciones.CodigoPostal = CodigoPostal
        direcciones.Distrito = Distrito
        direcciones.CodigoDomFiscal = CodigoDomFiscal
        direcciones.DireccionPrincipal = DireccionPrincipal
        direcciones.Entrega = Entrega
        direcciones.DestinatarioMercEstandar = DestinatarioMercEstandar
        direcciones.DestinatarioFactura = DestinatarioFactura
        direcciones.Telefono = Telefono
        direcciones.CorreoElectronico = CorreoElectronico
        direcciones.SitioWeb =SitioWeb
        direcciones.save

    return redirect("../gestionDirecciones/"+IdCliente)


#def agregarClienteDireccion(request,codigo):
#    return render(request,"agregarClienteDireccion.html",{"cliente":codigo})

def get_paises(request):
    paises = list(Country.objects.values())
    if (len(paises)>0):
        data={'message':"Success", 'paises':paises}
    else:
        data={"message":"Not Found"}

    return JsonResponse(data)

def get_estados(request, codigo):
    estados = list(Region.objects.filter(IdCountry=codigo).values())
    if (len(estados)>0):
        data={'message':"Success", 'estados':estados}
    else:
        data={"message":"Not Found"}

    return JsonResponse(data)

def get_codigos(request, codigo):
    if RelReg_Edo.objects.filter(idRegion=codigo).exists():
        relregedo = RelReg_Edo.objects.get(idRegion=codigo)   
        c_estado = relregedo.c_estado
        codigos = list(Sepomex.objects.annotate(cnt=Count('D_codigo')).filter(C_estado=c_estado).values('cnt', 'D_codigo').order_by('D_codigo'))
    
        if (len(codigos)>0):
            data={'message':"Success", 'codigos':codigos}
        else:
            data={"message":"Not Found"}
    else:
            data={"message":"Not Found"}

    return JsonResponse(data)

def get_colonias(request, codigo):
    colonias = list(Sepomex.objects.filter(D_codigo=codigo).order_by('D_asenta').values())
    if (len(colonias)>0):
        data={'message':"Success", 'colonias':colonias}
    else:
        data={"message":"Not Found"}

    return JsonResponse(data)
