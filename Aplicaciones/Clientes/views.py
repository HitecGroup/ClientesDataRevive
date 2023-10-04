from django.http import JsonResponse
from django.shortcuts import redirect, render
from .models import *
from django.db.models import Count

# Create your views here.
def home(request):
    clientes = Clientes.objects.all() 
    return render(request, "gestionClientes.html",{"clientes":clientes})

def edicionCliente(request,codigo):
    cliente = Clientes.objects.get(IdCliente=codigo)
    fecha = cliente.FechaNacimiento
    #fechaNacimiento = datetime.strftime(fecha,'%d/%m/%Y')
    acliente = {"IdCliente":cliente.IdCliente, 
            "ClaveExterna":cliente.ClaveExterna,
            "NombreCliente":cliente.NombreCliente,
            "FechaNacimiento":fecha, 
            "Sector":cliente.Sector,
            "TipoEmpresa":cliente.TipoEmpresa,
            "TipoCliente":cliente.TipoCliente,
            "ClientePotencial":cliente.ClientePotencial,
            "Estado":cliente.Estado,
            "Duns":cliente.Duns,
            "Clasificacion":cliente.Clasificacion,
            "Division":cliente.Division,
            "subDivision":cliente.subDivision,
            "SucServicio":cliente.SucServicio,
            "RegionVts":cliente.RegionVts,
            "iDNielsen":cliente.iDNielsen,
            "NoTurnosC":cliente.NoTurnosC,
            "Tier":cliente.Tier,
            "FrecuenciaCompra":cliente.FrecuenciaCompra,
            "NoMaqConvenC":cliente.NoMaqConvenC,
            "NoMaqCNC_C":cliente.NoMaqCNC_C,
            "NoMaqHT_C":cliente.NoMaqHT_C,
            "MatUseCHMER":cliente.MatUseCHMER,
            "MatUseYIZUMI":cliente.MatUseYIZUMI,
            "MatUsoFab":cliente.MatUsoFab,
            "MatViruta":cliente.MatViruta,
            #"MatUsoCNC_Haas":cliente.MatUsoCNC_Haas,
            "ActPriFAB":cliente.ActPriFAB,
            "ActPriEDM":cliente.ActPriEDM,
            "ActPriEquipoCNC":cliente.ActPriEquipoCNC,
            #"ActPriEquipo":cliente.ActPriEquipo,
            "dSector":get_Sector(cliente.Sector),
            "dTipoCliente":get_TipoCliente(cliente.TipoCliente),
            "dClientePotencial":get_ClientePotencial(cliente.ClientePotencial),
            "dEstado":get_Estado(cliente.Estado),
            "dClasificacion":get_Clasificacion(cliente.Clasificacion),
            "dDivision":get_Division(cliente.Division),
            "dsubDivision":get_SubDivision(cliente.subDivision),
            "dSucServicio":get_sucServicio(cliente.SucServicio),
            "dTipoEmpresa":get_TipoEmpresa(cliente.TipoEmpresa),
            "dTier":get_Tier(cliente.Tier),
            "dMatUseCHMER":get_MatUseCHMER(cliente.MatUseCHMER),
            "dMatUseYIZUMI":get_MatUseYIZUMI(cliente.MatUseYIZUMI),
            "dMatUsoFab":get_MatUsoFab(cliente.MatUsoFab),
            "dMatViruta":get_MatViruta(cliente.MatViruta),
            "dMatUsoCNC_Haas":get_MatUsoCNC_Haas(cliente.MatUsoCNC_Haas),
            "dRegionVts":get_RegionVts(cliente.RegionVts),
            "dActPriFAB":get_ActPriFAB(cliente.ActPriFAB),
            "dActPriEDM":get_ActPriEDM(cliente.ActPriEDM),
            "dActPriEquipoCNC":get_ActPriEquipoCNC(cliente.ActPriEquipoCNC),
            "dActPriEquipo":get_ActPriEquipo(cliente.ActPriEquipo),
            #"DireccioCliente":cliente.DireccioCliente,
            #"TelefonoPrincipal":cliente.TelefonoPrincipal,
            #"RFC":cliente.RFC,
            #"NombreAdicional":cliente.NombreAdicional,
            #"DivisionPM":cliente.DivisionPM,
            }
    
    return render(request, "edicionCliente.html",{"cliente":acliente})

def editarCliente(request):
    IdCliente = request.POST['claveExterna']
    NombreCliente = request.POST['NombreCliente']
    TipoCliente = request.POST['TipoCliente']
    ClientePotencial = request.POST['ClientePotencial']
    FechaNacimiento = request.POST['FechaNacimiento']
    Sector = request.POST['Sector']
    TipoCliente = request.POST['TipoCliente']
    ClientePotencial = request.POST['ClientePotencial']
    Estado = request.POST['Estado']
    Duns = request.POST['Duns']
    Clasificacion = request.POST['Clasificacion']
    Division = request.POST['Division']
    subDivision = request.POST['subDivision']
    zonaServicio = request.POST['SucServicio']
    TipoEmpresa = request.POST['TipoEmpresa']
    iDNielsen = request.POST['iDNielsen']
    RegionVts = request.POST['RegionVts']
    NoTurnosC = request.POST['NoTurnosC']
    Tier = request.POST['Tier']
    NoMaqConvenC = request.POST['NoMaqConvenC']
    NoMaqCNC_C = request.POST['NoMaqCNC_C']
    NoMaqHT_C = request.POST['NoMaqHT_C']

    MatUseCHMER = MatUseYIZUMI = MatUsoFab = MatViruta = ""
    if "MatUseCHMER" in request.POST:
        MatUseCHMER = request.POST['MatUseCHMER']
    if "MatUseYIZUMI" in request.POST:
        MatUseYIZUMI = request.POST['MatUseYIZUMI']
    if "MatUsoFab" in request.POST:
        MatUsoFab = request.POST['MatUsoFab']
    if "MatViruta" in request.POST:
        MatViruta = request.POST['MatViruta']
    #if "MatUseYIZUMI" in request.POST:
        #MatUsoCNC_Haas = request.POST['MatUsoCNC_Haas']

    FrecuenciaCompra = request.POST['FrecuenciaCompra']
    RegionVts = request.POST['RegionVts']

    ActPriFAB = ActPriEDM = ActPriEquipoCNC = ""
    #ActPriEquipo = ""
    if "ActPriFAB" in request.POST:
        ActPriFAB = request.POST['ActPriFAB']
    if "ActPriEDM" in request.POST:
        ActPriEDM = request.POST['ActPriEDM']
    if "ActPriEquipoCNC" in request.POST:
        ActPriEquipoCNC = request.POST['ActPriEquipoCNC']
    #if "ActPriEquipo" in request.POST:
        #ActPriEquipo = request.POST['ActPriEquipo']
    
    cliente = Clientes.objects.get(IdCliente=IdCliente)
    cliente.NombreCliente = NombreCliente
    cliente.FechaNacimiento = FechaNacimiento
    cliente.Sector = Sector
    cliente.TipoCliente = TipoCliente
    cliente.ClientePotencial = ClientePotencial
    cliente.Estado = Estado
    cliente.Duns = Duns
    cliente.Clasificacion = Clasificacion
    cliente.Division = Division
    cliente.subDivision = subDivision
    cliente.SucServicio = zonaServicio
    cliente.TipoEmpresa = TipoEmpresa
    cliente.iDNielsen= iDNielsen
    cliente.NoTurnosC = NoTurnosC
    cliente.Tier = Tier
    cliente.NoMaqConvenC = NoMaqConvenC
    cliente.NoMaqCNC_C = NoMaqCNC_C
    cliente.NoMaqHT_C = NoMaqHT_C
    cliente.MatUseCHMER = MatUseCHMER
    cliente.MatUseYIZUMI = MatUseYIZUMI
    cliente.MatUsoFab = MatUsoFab
    cliente.MatViruta = MatViruta
    #cliente.MatUsoCNC_Haas = MatUsoCNC_Haas
    cliente.FrecuenciaCompra = FrecuenciaCompra
    cliente.RegionVts = RegionVts
    cliente.ActPriFAB = ActPriFAB
    cliente.ActPriEDM = ActPriEDM
    cliente.ActPriEquipoCNC = ActPriEquipoCNC
    #cliente.ActPriEquipo = ActPriEquipo
    cliente.save()

    return redirect('/')

def gestionContactos(request,codigo):
    cliente = Clientes.objects.get(IdCliente=codigo)
    if Contactos.objects.filter(IdCliente=codigo).exists():
    # Si el cliente tiene contactos envía el listado de contactos del cliente
        contactosListados = Contactos.objects.all().filter(IdCliente=codigo)
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
        return render(request, "edicionContactos.html",{"vista":"Contacto", "Gestion":False, "idRegistro":"0", "contacto":contacto, "cliente":cliente, "iniPais":iniPais, "iniRegion":iniRegion, "iniCodPos":iniCodPos, "iniDistrito":iniDistrito, "dataInt":False, "iniCheckbox":iniCheckbox })

def edicionContacto(request, idCliente, codigo, Gestion):        
    cliente = Clientes.objects.get(IdCliente=idCliente)
    iniCodPos = ""
    iniDistrito = ""
    dataInt = False
    flag1 = flag2 = False
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

        if( contacto.Principal ):
            flag1 = True
        if( contacto.Vip == "1" ):
            flag2 = True

    iniCheckbox = {"Principal":flag1, "VIP":flag2}
    
    return render(request, "edicionContactos.html",{"vista":"Contacto", "Gestion":Gestion, "idRegistro":codigo, "contacto":contacto, "cliente":cliente, "iniPais":iniPais, "iniRegion":iniRegion, "iniCodPos":iniCodPos, "iniDistrito":iniDistrito, "dataInt":dataInt, "iniCheckbox":iniCheckbox })

def editarContacto(request):
    IdCliente = request.POST['IdCliente']
    IdContacto = request.POST['idRegistro']
    NombreContacto = request.POST['Nombre']
    SegundoNombre = request.POST['SegundoNombre']
    Apellidos = request.POST['Apellidos']
    Telefono = request.POST['Telefono']
    TelefonoMovil = request.POST['TelefonoMovil']
    CorreoElectronico = request.POST['CorreoElectronico']
    Departamento = request.POST['Departamento']
    Funcion = request.POST['Funcion']
    PaisRegion = request.POST['PaisRegion']
    Estado = request.POST['Estado']

    if (PaisRegion=="MX"):
        CodigoPostal = request.POST['CodigoPostal']
        Ciudad = request.POST['Ciudad']
        Distrito = request.POST['Distrito']
    else :
        CodigoPostal = request.POST['IntCodigoPostal']
        Ciudad = request.POST['IntCiudad']
        Distrito = request.POST['IntDistrito']  

    Calle = request.POST['Calle']
    Numero = request.POST['Numero']
    Edificio = request.POST['Edificio']
    Planta = request.POST['Planta']
    PaisExp = request.POST['PaisExp']
    MedioComunicacion = request.POST['MedioComunicacion']

    Principal = Vip = 0
    
    if "Principal" in request.POST:
        Principal = 1    
    if 'VIP' in request.POST:
        Vip = 1

    if(IdContacto != "0") :
        contacto = Contactos.objects.get(IdContacto=IdContacto)
        contacto.Nombre = NombreContacto
        contacto.SegundoNombre = SegundoNombre
        contacto.Apellidos = Apellidos
        contacto.Telefono = Telefono
        contacto.TelefonoMovil = TelefonoMovil
        contacto.CorreoElectronico = CorreoElectronico
        contacto.Departamento = Departamento
        contacto.Funcion = Funcion
        contacto.PaisRegion = PaisRegion
        contacto.Estado = Estado
        contacto.CodigoPostal = CodigoPostal
        contacto.Ciudad = Ciudad
        contacto.Distrito = Distrito
        contacto.Calle = Calle
        contacto.Numero = Numero
        contacto.Edificio = Edificio
        contacto.Planta = Planta
        contacto.PaisExp = PaisExp
        contacto.MedioComunicacion = MedioComunicacion
        contacto.Principal = Principal
        contacto.Vip = Vip    
        contacto.save()

    else :
        ultimo = Contactos.objects.order_by('-IdContacto').first()
        IdContacto = ultimo.IdContacto

        contacto = Contactos.objects.create (
            IdContacto = str(int(IdContacto)+1),
            IdCliente = IdCliente,
            Nombre = NombreContacto,
            SegundoNombre = SegundoNombre,
            Apellidos = Apellidos,
            Telefono = Telefono,
            TelefonoMovil = TelefonoMovil,
            CorreoElectronico = CorreoElectronico,
            Departamento = Departamento,
            Funcion = Funcion,
            PaisRegion = PaisRegion,
            Estado = Estado,
            CodigoPostal = CodigoPostal,
            Ciudad = Ciudad,
            Distrito = Distrito,
            Calle = Calle,
            Numero = Numero,
            Edificio = Edificio,
            Planta = Planta,
            PaisExp = PaisExp,
            MedioComunicacion = MedioComunicacion,
            Principal = Principal,
            Vip = Vip,
            Bloqueo = 0
        )
            
    cliente = Clientes.objects.get(IdCliente=IdCliente)
    contactosListados = Contactos.objects.all().filter(IdCliente=IdCliente)
    return render(request,"gestionContactos.html",{"contactos":contactosListados, "cliente":cliente})

def bloquearContacto(request, codigo,cliente):

    contacto = Contactos.objects.get(IdContacto=codigo)

    if contacto.Bloqueo != True:

        contacto.Bloqueo = True

    else:

        contacto.Bloqueo = False

    contacto.save()

 

    contactosListados = Contactos.objects.all().filter(IdCliente=cliente)

 

    return render(request,"gestionContactos.html",{"contactos":contactosListados, "cliente":cliente})

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
    Estado = request.POST['Estado']

    CodigoDomFiscal = ""
    if(PaisRegion=="MX"):
        CodigoPostal = request.POST['CodigoPostal']
        Ciudad = request.POST['Ciudad']
        Distrito = request.POST['Distrito']
    else :
        CodigoPostal = request.POST['IntCodigoPostal']
        Ciudad = request.POST['IntCiudad']
        Distrito = request.POST['IntDistrito']
        if(PaisRegion=="US"):
            CodigoDomFiscal = request.POST['CodigoDomFiscal']
    
    Calle = request.POST['Calle']
    Numero = request.POST['Numero']
    Calle2 = request.POST['Calle2']
    CodigoDomFiscal = ""
    Telefono = request.POST['Telefono']
    CorreoElectronico = request.POST['CorreoElectronico']
    SitioWeb = request.POST['SitioWeb']   

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
    
    if (idRegistro != "0") :
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
        direcciones.save()

    else :
        ultimo = Direcciones.objects.order_by('-IdRegistro').first()
        idRegistro = ultimo.IdRegistro

        direcciones = Direcciones.objects.create (
            IdCliente = IdCliente,
            PaisRegion = PaisRegion,
            Calle = Calle,
            Numero = Numero,
            Calle2 = Calle2,
            Ciudad = Ciudad,
            Estado = Estado,
            CodigoPostal = CodigoPostal,
            Distrito = Distrito,
            CodigoDomFiscal = CodigoDomFiscal,
            DireccionPrincipal = DireccionPrincipal,
            Entrega = Entrega,
            DestinatarioMercEstandar = DestinatarioMercEstandar,
            DestinatarioFactura = DestinatarioFactura,
            Telefono = Telefono,
            CorreoElectronico = CorreoElectronico,
            SitioWeb =SitioWeb,
            Bloqueo = 0
        )

    return redirect("../gestionDirecciones/"+IdCliente)

def bloquearDireccion(request, cliente,idDireccion):

    direccion = Direcciones.objects.get(IdRegistro=idDireccion)

    if direccion.Bloqueo != True:

        direccion.Bloqueo = True

    else:

        direccion.Bloqueo = False

    direccion.save()

    direccionesListados = Direcciones.objects.all().filter(IdCliente=cliente)

    cliente = Clientes.objects.get(IdCliente=cliente)

 
    return render(request,"gestionDirecciones.html",{"direcciones":direccionesListados, "cliente":cliente})

 

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


def get_Sector(codigo):
    descrip = ""
    if(codigo=="11"):            descrip = "Agrícola"
    elif (codigo == '22') :      descrip = 'Servicios públicos'
    elif (codigo == '23') :      descrip = 'Construcción'
    elif (codigo == '31') :      descrip = 'Fabricación'
    elif (codigo == '42') :      descrip = 'Comercio mayorista'
    elif (codigo == '44') :      descrip = 'Comercio minorista'
    elif (codigo == '48') :      descrip = 'Transporte y almacenamiento'
    elif (codigo == '51') :      descrip = 'Información'
    elif (codigo == '52') :      descrip = 'Finanzas y seguro'
    elif (codigo == '53') :      descrip = 'Bienes inmuebles, alquiler y leasing'
    elif (codigo == '54') :      descrip = 'Servicios profesionales, científicos y técnicos'
    elif (codigo == '55') :      descrip = 'Gestión de compañías y empresas'
    elif (codigo == '56') :      descrip = 'Servicios de recuperación, gestión de desechos y soporte administrativo'
    elif (codigo == '61') :      descrip = 'Servicios educativos'
    elif (codigo == '62') :      descrip = 'Atención médica y asistencia social'
    elif (codigo == '71') :      descrip = 'Arte, entretenimiento y recreación'
    elif (codigo == '72') :      descrip = 'Servicios de alimentación y alojamiento'
    elif (codigo == '81') :      descrip = 'Otros servicios (excepto administración pública)'
    elif (codigo == '92') :      descrip = 'Administración pública'
    elif (codigo == 'Z01') :      descrip = 'Aeroespacial y Aeronáutica'
    elif (codigo == 'Z02') :      descrip = 'Alimentos y bebidas'
    elif (codigo == 'Z03') :      descrip = 'Artículos y Maquinaria Industrial'
    elif (codigo == 'Z04') :      descrip = 'Automotriz'
    elif (codigo == 'Z05') :      descrip = 'Bearings'
    elif (codigo == 'Z06') :      descrip = 'Bombas y válvulas otras'
    elif (codigo == 'Z07') :      descrip = 'Bombas y válvulas PET'
    elif (codigo == 'Z08') :      descrip = 'Calzado'
    elif (codigo == 'Z10') :      descrip = 'Corte lámina'
    elif (codigo == 'Z11') :      descrip = 'Educación'
    elif (codigo == 'Z12') :      descrip = 'Eléctrico'
    elif (codigo == 'Z13') :      descrip = 'Entretenimiento y Deportes'
    elif (codigo == 'Z14') :      descrip = 'Estructuras y Perfiles'
    elif (codigo == 'Z15') :      descrip = 'Farmacéutico'
    elif (codigo == 'Z16') :      descrip = 'Ferrocarril'
    elif (codigo == 'Z17') :      descrip = 'Forja'
    elif (codigo == 'Z18') :      descrip = 'Funcición'
    elif (codigo == 'Z19') :      descrip = 'Generación de Energía'
    elif (codigo == 'Z20') :      descrip = 'Gobierno'
    elif (codigo == 'Z21') :      descrip = 'Herramientas y utillaje'
    elif (codigo == 'Z22') :      descrip = 'Instrumental de precisión'
    elif (codigo == 'Z23') :      descrip = 'Joyería'
    elif (codigo == 'Z24') :      descrip = 'Línea blanca'
    elif (codigo == 'Z25') :      descrip = 'Mantenimiento'
    elif (codigo == 'Z26') :      descrip = 'Médico'
    elif (codigo == 'Z27') :      descrip = 'Militar'
    elif (codigo == 'Z28') :      descrip = 'Minera'
    elif (codigo == 'Z29') :      descrip = 'Moldes, troqueles y matrices'
    elif (codigo == 'Z30') :      descrip = 'Muebles'
    elif (codigo == 'Z31') :      descrip = 'Naval'
    elif (codigo == 'Z33') :      descrip = 'Otras'
    elif (codigo == 'Z34') :      descrip = 'Papelelero'
    elif (codigo == 'Z35') :      descrip = 'Petróleo y Gas'
    elif (codigo == 'Z36') :      descrip = 'Plástico'
    elif (codigo == 'Z37') :      descrip = 'Prensado'
    elif (codigo == 'Z38') :      descrip = 'Químico'
    elif (codigo == 'Z39') :      descrip = 'Robótica y automatización'
    elif (codigo == 'Z40') :      descrip = 'Textil'
    elif (codigo == 'Z41') :      descrip = 'Taller/Maquiladora'
    else :                        descrip = ""

    return (descrip)

def get_ClientePotencial(codigo) :
    if (codigo == '1') :   descrip = 'Si'
    else :                  descrip = 'No'

    return (descrip)

def get_Estado(codigo) :
    if (codigo == '1') :   descrip = 'Activo'
    else :                  descrip = 'Inactivo'

    return (descrip)

def get_Clasificacion(codigo) :
    if (codigo == 'A') :        descrip = 'HTAAA'
    elif (codigo == 'B') :      descrip = 'HTAA'
    elif (codigo == 'C') :      descrip = 'HTA'
    elif (codigo == 'L') :      descrip = 'PAAA'
    elif (codigo == 'M') :      descrip = 'PAA'
    elif (codigo == 'N') :      descrip = 'PA'
    elif (codigo == 'O') :      descrip = 'PB'
    else :                      descrip = ''

    return (descrip)

def get_TipoCliente(codigo) :
    if (codigo == 'Particular') :   descrip = 'Particular'
    elif (codigo == 'Corporativo') : descrip = 'Corporativo' 
    else :                  descrip = ''

    return (descrip)

def get_Division(codigo) :
    if   (codigo == 'Haas CAM') :      descrip = 'Haas CAM'
    elif (codigo == 'Haas Colombia') :      descrip = 'Haas Colombia'
    elif (codigo == 'Haas Ecuador') :      descrip = 'Haas Ecuador'
    elif (codigo == 'Haas México') :      descrip = 'Haas México'
    elif (codigo == 'Hitec CNC Maquinaria de México') :      descrip = 'Hitec CNC Maquinaria de México'
    elif (codigo == 'Hitec Tools') :      descrip = 'Hitec Tools'
    elif (codigo == 'Nexttec Machinery') :      descrip = 'Nexttec Machinery'
    elif (codigo == 'A&G Plastic Machinery') :      descrip = 'A&G Plastic Machinery'
    else :      descrip = ''

    return (descrip)

def get_SubDivision(codigo) :
    if   (codigo == 'HFO') :      descrip = 'HFO'
    elif (codigo == 'CNC') :      descrip = 'CNC'
    elif (codigo == 'OT') :      descrip = 'OT'
    elif (codigo == 'Htools') :      descrip = 'Htools'
    elif (codigo == 'EDM') :      descrip = 'EDM'
    elif (codigo == 'FAB') :      descrip = 'FAB'
    elif (codigo == 'PM') :      descrip = 'PM'
    else :      descrip = ''

    return (descrip)

def get_sucServicio(codigo) :
    if   (codigo == '101') :      descrip = 'MX - Cd. Juárez'
    elif (codigo == '102') :      descrip = 'MX - Celaya'
    elif (codigo == '103') :      descrip = 'MX - Chihuahua'
    elif (codigo == '104') :      descrip = 'MX - Guadalajara'
    elif (codigo == '105') :      descrip = 'MX - León'
    elif (codigo == '106') :      descrip = 'MX - Mexicali'
    elif (codigo == '107') :      descrip = 'MX - México'
    elif (codigo == '108') :      descrip = 'MX - Monterrey'
    elif (codigo == '109') :      descrip = 'MX - Puebla'
    elif (codigo == '110') :      descrip = 'MX - Querétaro'
    elif (codigo == '111') :      descrip = 'MX - Saltillo'
    elif (codigo == '112') :      descrip = 'MX - San Luis Potosí'
    elif (codigo == '113') :      descrip = 'MX - Sonora'
    elif (codigo == '114') :      descrip = 'MX - Tamaulipas'
    elif (codigo == '115') :      descrip = 'MX - Tijuana'
    elif (codigo == '116') :      descrip = 'MX -Toluca'
    elif (codigo == '117') :      descrip = 'MX - Torreón'
    elif (codigo == '118') :      descrip = 'CO - Bogotá'
    elif (codigo == '119') :      descrip = 'ES - Barcelona'
    elif (codigo == '120') :      descrip = 'ES - Madrid'
    elif (codigo == '121') :      descrip = 'ES - Sevilla'
    elif (codigo == '122') :      descrip = 'ES - Valencia'
    elif (codigo == '123') :      descrip = 'ES - Vitoria'
    elif (codigo == '124') :      descrip = 'EC - Guayaquil'
    elif (codigo == '125') :      descrip = 'CO - Medellín'
    elif (codigo == '126') :      descrip = 'CO - Cartagena'
    elif (codigo == '127') :      descrip = 'CO - Cali'
    elif (codigo == '128') :      descrip = 'CO - Manizales'
    elif (codigo == '129') :      descrip = 'CR - Costa Rica'
    elif (codigo == '130') :      descrip = 'HO - Tegucigalpa'
    elif (codigo == '131') :      descrip = 'GU - Guatemala'
    elif (codigo == '132') :      descrip = 'SA - El Salvador'
    elif (codigo == '133') :      descrip = 'EC - Quito'
    elif (codigo == '134') :      descrip = 'EC - Francisco de Orellana'
    elif (codigo == '135') :      descrip = 'EC - Ambato'
    elif (codigo == '136') :      descrip = 'EC - Cuenca'
    elif (codigo == '137') :      descrip = 'HO - San Pedro Sula'
    elif (codigo == '138') :      descrip = 'NI - Managua'
    elif (codigo == '139') :      descrip = 'NI - León'
    else :  descrip = ''

    return (descrip)

def get_TipoEmpresa(codigo) :
    if   (codigo == '193') :      descrip = 'Producto propio'
    elif (codigo == '194') :      descrip = 'Maquiladora'
    elif (codigo == '195') :      descrip = 'Gobierno'
    elif (codigo == '196') :      descrip = 'Educación'
    else :  descrip = ''

    return (descrip)

def get_Tier(codigo) :
    if   (codigo == '197') :      descrip = 'Tier 1'
    elif (codigo == '198') :      descrip = 'Tier 2'
    elif (codigo == '199') :      descrip = 'Tier 3'
    elif (codigo == '200') :      descrip = 'Gobierno'
    elif (codigo == '201') :      descrip = 'N/A'
    else :  descrip = ''

    return (descrip)

def get_MatUseCHMER(codigo) :
    if   (codigo == '170') :      descrip = 'Aceros al carbón'
    elif (codigo == '171') :      descrip = 'Acero inoxidable'
    elif (codigo == '172') :      descrip = 'Carburo de tuxteno'
    elif (codigo == '173') :      descrip = 'No Ferrosos'
    elif (codigo == '174') :      descrip = 'Aleaciones Especiales'
    elif (codigo == '175') :      descrip = 'Fundición'
    elif (codigo == '176') :      descrip = 'Varios'
    else :  descrip = ''

    return (descrip)

def get_MatUseYIZUMI(codigo) :
    if   (codigo == '179') :      descrip = 'PETE (Polietileno tereftalato)'
    elif (codigo == '180') :      descrip = 'HDPE (Polietileno de alta densidad)'
    elif (codigo == '181') :      descrip = 'V (Policloruro de vinilo)'
    elif (codigo == '182') :      descrip = 'LDPE (Polietileno de baja densidad)'
    elif (codigo == '183') :      descrip = 'PP (Polipropileno)'
    elif (codigo == '184') :      descrip = 'PS (Poliestireno)'
    elif (codigo == '185') :      descrip = 'Otros Plásticos, resinas, composites'
    else :  descrip = ''

    return (descrip)

def get_RegionVts(codigo) :
    if   (codigo == '101') :      descrip = 'MX - Cd. Juárez'
    elif (codigo == '102') :      descrip = 'MX - Celaya'
    elif (codigo == '103') :      descrip = 'MX - Chihuahua'
    elif (codigo == '104') :      descrip = 'MX - Guadalajara'
    elif (codigo == '105') :      descrip = 'MX - León'
    elif (codigo == '106') :      descrip = 'MX - Mexicali'
    elif (codigo == '107') :      descrip = 'MX - México'
    elif (codigo == '108') :      descrip = 'MX - Monterrey'
    elif (codigo == '109') :      descrip = 'MX - Puebla'
    elif (codigo == '110') :      descrip = 'MX - Querétaro'
    elif (codigo == '111') :      descrip = 'MX - Saltillo'
    elif (codigo == '112') :      descrip = 'MX - San Luis Potosí'
    elif (codigo == '113') :      descrip = 'MX - Sonora'
    elif (codigo == '114') :      descrip = 'MX - Tamaulipas'
    elif (codigo == '115') :      descrip = 'MX - Tijuana'
    elif (codigo == '116') :      descrip = 'MX -Toluca'
    elif (codigo == '117') :      descrip = 'MX - Torreón'
    elif (codigo == '118') :      descrip = 'CO - Bogotá'
    elif (codigo == '119') :      descrip = 'ES - Barcelona'
    elif (codigo == '120') :      descrip = 'ES - Madrid'
    elif (codigo == '121') :      descrip = 'ES - Sevilla'
    elif (codigo == '122') :      descrip = 'ES - Valencia'
    elif (codigo == '123') :      descrip = 'ES - Vitoria'
    elif (codigo == '124') :      descrip = 'EC - Guayaquil'
    elif (codigo == '125') :      descrip = 'CO - Medellín'
    elif (codigo == '126') :      descrip = 'CO - Cartagena'
    elif (codigo == '127') :      descrip = 'CO - Cali'
    elif (codigo == '128') :      descrip = 'CO - Manizales'
    elif (codigo == '129') :      descrip = 'CR - Costa Rica'
    elif (codigo == '130') :      descrip = 'HO - Tegucigalpa'
    elif (codigo == '131') :      descrip = 'GU - Guatemala'
    elif (codigo == '132') :      descrip = 'SA - El Salvador'
    elif (codigo == '133') :      descrip = 'EC - Quito'
    elif (codigo == '134') :      descrip = 'EC - Francisco de Orellana'
    elif (codigo == '135') :      descrip = 'EC - Ambato'
    elif (codigo == '136') :      descrip = 'EC - Cuenca'
    elif (codigo == '137') :      descrip = 'HO - San Pedro Sula'
    elif (codigo == '138') :      descrip = 'NI - Managua'
    elif (codigo == '139') :      descrip = 'NI - León'
    else :  descrip = ''

    return (descrip)

def get_RegionVts(codigo) :
    if   (codigo == '109') :      descrip = 'MX - HFO SURESTE'
    elif (codigo == '110') :      descrip = 'MX - HFO NORTE'
    elif (codigo == '111') :      descrip = 'MX - HFO BAJIO'
    elif (codigo == '112') :      descrip = 'MX - HFO PACIFICO OCCIDENTE'
    elif (codigo == '113') :      descrip = 'MX - HFO CENTRO'
    elif (codigo == '114') :      descrip = 'CENTRO AMERICA'
    elif (codigo == '115') :      descrip = 'MX - PLASTICOS'
    elif (codigo == '117') :      descrip = 'ES - HFO NORESTE'
    elif (codigo == '118') :      descrip = 'ES - HFO LEVANTE'
    elif (codigo == '119') :      descrip = 'ES - HFO SUR'
    elif (codigo == '120') :      descrip = 'ES - HFO CENTRO'
    elif (codigo == '121') :      descrip = 'ES - HFO NORTE'
    else :  descrip = ''

    return (descrip)

def get_ActPriFAB(codigo) :
    if   (codigo == '146') :      descrip = 'Estructuras metálicas"'
    elif (codigo == '147') :      descrip = 'Bridas, valvulas,conexiones, sellos, rodamientos, tubos, coples"'
    elif (codigo == '148') :      descrip = 'Herramientas"'
    elif (codigo == '149') :      descrip = 'Maquinado de partes"'
    elif (codigo == '150') :      descrip = 'Transformación de piezas de fundición"'
    elif (codigo == '151') :      descrip = 'Maquinas, Equipos y automatización"'
    elif (codigo == '152') :      descrip = 'Prototipos"'
    elif (codigo == '153') :      descrip = 'Troqueles y Matrices"'
    elif (codigo == '154') :      descrip = 'Transformación de lamina"'
    elif (codigo == '155') :      descrip = 'Estantería y Mobiliario Publico"'
    elif (codigo == '156') :      descrip = 'Distribuidores de acero"'
    elif (codigo == '157') :      descrip = 'Carrocerías / Remolques de marca propia"'
    elif (codigo == '158') :      descrip = 'Paileria"'
    elif (codigo == '159') :      descrip = 'Básculas / Fabricantes de básculas"'
    elif (codigo == '160') :      descrip = 'Fabricantes de Piezas Metálicas en serie"'
    elif (codigo == '161') :      descrip = 'Ductos de Lámina / Ductos para aire / Recolectores de Polvo / Filtros Industriales."'
    else :  descrip = ''

    return (descrip)

def get_ActPriEquipoCNC(codigo) :
    if   (codigo == '106') :      descrip = 'Anclas, estructuras metálicas'
    elif (codigo == '107') :      descrip = 'Bridas, valvulas,conexiones, sellos, rodamientos, tubos, coples'
    elif (codigo == '108') :      descrip = 'Dados de extrusión'
    elif (codigo == '109') :      descrip = 'Dispositivos , gages, herramentales'
    elif (codigo == '110') :      descrip = 'Grabado'
    elif (codigo == '111') :      descrip = 'Herramientas'
    elif (codigo == '112') :      descrip = 'Investigación, desarrollo, enseñanza'
    elif (codigo == '113') :      descrip = 'Maquinado de partes'
    elif (codigo == '114') :      descrip = 'Maquinado de piezas de fundición'
    elif (codigo == '115') :      descrip = 'Maquinas, Equipos y automatización'
    elif (codigo == '116') :      descrip = 'Moldes'
    elif (codigo == '117') :      descrip = 'Partes para mantenimiento'
    elif (codigo == '118') :      descrip = 'Prototipos'
    elif (codigo == '119') :      descrip = 'Tornillos y tuercas'
    elif (codigo == '120') :      descrip = 'Troqueles y Matrices'
    elif (codigo == '121') :      descrip = 'Turbinas'
    elif (codigo == '122') :      descrip = 'Otros'
    else :  descrip = ''

    return (descrip)

def get_MatUsoFab(codigo) :
    if   (codigo == '187') :      descrip = 'Aluminio'
    elif (codigo == '188') :      descrip = 'Acero'
    elif (codigo == '189') :      descrip = 'Acero inoxidable'
    elif (codigo == '190') :      descrip = 'No Ferrosos'
    elif (codigo == '191') :      descrip = 'Lámina'
    else :  descrip = ''

    return (descrip)

def get_MatViruta(codigo) :
    if   (codigo == '163') :      descrip = 'Aceros al carbón'
    elif (codigo == '164') :      descrip = 'Acero inoxidable'
    elif (codigo == '165') :      descrip = 'Fundición'
    elif (codigo == '166') :      descrip = 'No Ferrosos'
    elif (codigo == '167') :      descrip = 'Aleaciones Especiales'
    elif (codigo == '168') :      descrip = 'Varios'
    else :  descrip = ''

    return (descrip)

def get_MatUsoCNC_Haas(codigo) :
    if   (codigo == '163') :      descrip = 'Aceros al carbón'
    elif (codigo == '164') :      descrip = 'Acero inoxidable'
    elif (codigo == '165') :      descrip = 'Fundición'
    elif (codigo == '166') :      descrip = 'No Ferrosos'
    elif (codigo == '167') :      descrip = 'Aleaciones Especiales'
    elif (codigo == '168') :      descrip = 'Varios'
    else :  descrip = ''

    return (descrip)


def get_ActPriEDM(codigo) :
    if   (codigo == '124') :      descrip = 'Moldes'
    elif (codigo == '125') :      descrip = 'Troqueles y Matrices'
    elif (codigo == '126') :      descrip = 'Grabado'
    elif (codigo == '127') :      descrip = 'Dispositivos , gages'
    elif (codigo == '128') :      descrip = 'Herramentales especiales'
    else :  descrip = ''

    return (descrip)

def get_ActPriEquipo(codigo) :
    if   (codigo == '106') :      descrip = 'Anclas, estructuras metálicas'
    elif (codigo == '107') :      descrip = 'Bridas, valvulas,conexiones, sellos, rodamientos, tubos, coples'
    elif (codigo == '108') :      descrip = 'Dados de extrusión'
    elif (codigo == '109') :      descrip = 'Dispositivos , gages, herramentales'
    elif (codigo == '110') :      descrip = 'Grabado'
    elif (codigo == '111') :      descrip = 'Herramientas'
    elif (codigo == '112') :      descrip = 'Investigación, desarrollo, enseñanza'
    elif (codigo == '113') :      descrip = 'Maquinado de partes'
    elif (codigo == '114') :      descrip = 'Maquinado de piezas de fundición'
    elif (codigo == '115') :      descrip = 'Maquinas, Equipos y automatización'
    elif (codigo == '116') :      descrip = 'Moldes'
    elif (codigo == '117') :      descrip = 'Partes para mantenimiento'
    elif (codigo == '118') :      descrip = 'Prototipos'
    elif (codigo == '119') :      descrip = 'Tornillos y tuercas'
    elif (codigo == '120') :      descrip = 'Troqueles y Matrices'
    elif (codigo == '121') :      descrip = 'Turbinas'
    elif (codigo == '122') :      descrip = 'Otros'
    else :  descrip = ''

    return (descrip)