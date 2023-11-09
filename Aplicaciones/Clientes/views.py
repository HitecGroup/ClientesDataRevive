from django.http import JsonResponse
from django.shortcuts import redirect, render
from .models import *
from django.db.models import Count
from django.db.models import Q
from datetime import datetime
from django.contrib import messages

# Create your views here.
def home(request, usrid=0):
    session = getSession(usrid)
    
    clientesOk = []
    clientes = Clientes.objects.all()[0:200]
    for item in clientes.iterator():
        item.RegionVts = get_RegionVts(item.RegionVts)
        clientesOk.append(item)

    return render(request, "gestionClientes.html",{"clientes":clientesOk, "session":session})
 
def login(request):
    return render(request, "login.html")

def cambiarPwd(request):
    return render(request, "cambiarPwd.html")

def cambioPwd(request):
    user = request.POST['user']
    pwd = request.POST['pwd']
    newpwd = request.POST['newpwd']
    ruta = "cambiarPwd.html"

    if Users.objects.filter(User=user).exists():
        usuario = Users.objects.get(User=user)
        if(pwd==usuario.Pwd):
            usuario.Pwd = newpwd
            usuario.save()
            msg = 'La contraseña fue cambiada con éxito.'
        else :
            msg = 'La contraseña es incorrecta.  Intente de nuevo.'
    else:
        msg = 'El usuario no existe.  Revise e intente de nuevo.'

    return render(request, ruta, {"msg":msg})

def loginUsr(request):
    user = request.POST['user']
    pwd = request.POST['pwd']

    usrvalid = False
    usrid = 0
    usuario = nombre = msg = ""

    if Users.objects.filter(User=user).exists():
        usuario = Users.objects.get(User=user)
        if(pwd==usuario.Pwd):
            usrvalid = True
            usrid = usuario.Id      
            nombre = usuario.Nombre
            
            clientesOk = []
            clientes = Clientes.objects.all()[0:200]
            for item in clientes.iterator():
                item.RegionVts = get_RegionVts(item.RegionVts)
                clientesOk.append(item)

            session = {'usrvalid':usrvalid, 'usrid': usrid, 'user':user, 'nombre':nombre, 'msg':msg}
            return render(request, "gestionClientes.html",{"clientes":clientesOk, "session":session})
        else :
            msg = 'La contraseña es incorrecta.  Intente de nuevo.'
    else:
        msg = 'El usuario no existe.  Revise e intente de nuevo.'
      
    session = {'usrvalid':usrvalid, 'usrid': usrid, 'user':user, 'nombre':nombre, 'msg':msg}
    return render(request, 'login.html',{'session':session})

def getSession(usrid):
    usrvalid = False
    user = ""
    msg = nombre = ""

    if Users.objects.filter(Id=usrid).exists():
        usuario = Users.objects.get(Id=usrid)
        usrvalid = True
        user = usuario.User      
        nombre = usuario.Nombre

    return ({'usrvalid':usrvalid, 'usrid': usrid, 'user':user, 'nombre':nombre, 'msg':msg})

def edicionCliente(request, codigo, usrid):
    session = getSession(usrid)
    cliente = Clientes.objects.get(IdCliente=codigo)
    acliente = setDataCliente(cliente)
    
    return render(request, "edicionCliente.html",{"cliente":acliente, "session":session, "logData":getLogData('Clientes', codigo)})

def setDataCliente(cliente):
    fecha = cliente.FechaNacimiento
    DivHaasMexico = validDivision(cliente.IdCliente, 1, 109)
    DivHaasEcuador = validDivision(cliente.IdCliente, 1, 111)
    DivHaasColombia = validDivision(cliente.IdCliente, 1, 112)
    DivHaasCAM = validDivision(cliente.IdCliente, 1, 113)
    DivPM = validDivision(cliente.IdCliente, 2, 116)
    DivHToolsTools = validDivision(cliente.IdCliente, 3, 118)
    #DivHToolsSolubles = validDivision(cliente.IdCliente, 3, 119)
    DivCNCCNC = validDivision(cliente.IdCliente, 4, 121)
    DivCNCOmnitec = validDivision(cliente.IdCliente, 4, 122)
    DivNextecFAB = validDivision(cliente.IdCliente, 5, 123)
    DivNextecEDM = validDivision(cliente.IdCliente, 5, 124)
    dRegionVts = get_RegionVts(cliente.RegionVts)

    acliente = {"IdCliente":cliente.IdCliente, 
            "ClaveExterna":cliente.ClaveExterna,
            "NombreCliente":cliente.NombreCliente,
            "FechaNacimiento":fecha, 
            "Sector":cliente.Sector,
            "TipoEmpresa":cliente.TipoEmpresa,
            #"TipoCliente":cliente.TipoCliente,
            #"ClientePotencial":cliente.ClientePotencial,
            "Estado":cliente.Estado,
            #"Duns":cliente.Duns,
            #"Clasificacion":cliente.Clasificacion,
            #"Division":cliente.Division,
            #"subDivision":cliente.subDivision,
            "DivHaasMexico":DivHaasMexico,
            "DivHaasEcuador":DivHaasEcuador,
            "DivHaasColombia":DivHaasColombia,
            "DivHaasCAM":DivHaasCAM,
            "DivPM":DivPM,
            "DivCNCCNC":DivCNCCNC,
            "DivCNCOmnitec":DivCNCOmnitec,
            "DivHToolsTools":DivHToolsTools,
            #"DivHToolsSolubles":DivHToolsSolubles,
            "DivNextecFAB":DivNextecFAB,
            "DivNextecEDM":DivNextecEDM,
            #"SucServicio":cliente.SucServicio,
            #"RegionVts":cliente.RegionVts,
            #"iDNielsen":cliente.iDNielsen,
            "NoTurnosC":cliente.NoTurnosC,
            "Tier":cliente.Tier,
            #"FrecuenciaCompra":cliente.FrecuenciaCompra,
            "NoMaqConvenC":cliente.NoMaqConvenC,
            #"NoMaqCNC_C":cliente.NoMaqCNC_C,
            #"NoMaqHT_C":cliente.NoMaqHT_C,
            "MatUseCHMER":cliente.MatUseCHMER,
            "MatUseYIZUMI":cliente.MatUseYIZUMI,
            "MatUsoFab":cliente.MatUsoFab,
            "MatViruta":cliente.MatViruta,
            #"MatUsoCNC_Haas":cliente.MatUsoCNC_Haas,
            #"ActPriFAB":cliente.ActPriFAB,
            #"ActPriEDM":cliente.ActPriEDM,
            #"ActPriEquipoCNC":cliente.ActPriEquipoCNC,
            #"ActPriEquipo":cliente.ActPriEquipo,
            "dSector":get_Sector(cliente.Sector),
            "dTipoCliente":get_TipoCliente(cliente.TipoCliente),
            #"dClientePotencial":get_ClientePotencial(cliente.ClientePotencial),
            "dEstado":get_Estado(cliente.Estado),
            "dClasificacion":get_Clasificacion(cliente.Clasificacion),
            "dDivision":get_Division(cliente.Division),
            "dsubDivision":get_SubDivision(cliente.subDivision),
            #"dSucServicio":get_sucServicio(cliente.SucServicio),
            "dTipoEmpresa":get_TipoEmpresa(cliente.TipoEmpresa),
            "dTier":get_Tier(cliente.Tier),
            "dMatUseCHMER":get_MatUseCHMER(cliente.MatUseCHMER),
            "dMatUseYIZUMI":get_MatUseYIZUMI(cliente.MatUseYIZUMI),
            "dMatUsoFab":get_MatUsoFab(cliente.MatUsoFab),
            "dMatViruta":get_MatViruta(cliente.MatViruta),
            "dMatUsoCNC_Haas":get_MatUsoCNC_Haas(cliente.MatUsoCNC_Haas),
            "dRegionVts":dRegionVts,
            #"dActPriFAB":get_ActPriFAB(cliente.ActPriFAB),
            #"dActPriEDM":get_ActPriEDM(cliente.ActPriEDM),
            #"dActPriEquipoCNC":get_ActPriEquipoCNC(cliente.ActPriEquipoCNC),
            #"dActPriEquipo":get_ActPriEquipo(cliente.ActPriEquipo),
            "dDivHaas":get_DivHaas(cliente.DivHaas),
            "dDivPM":get_DivPM(cliente.DivPM),
            "dDivCNC":get_DivCNC(cliente.DivCNC),
            "dDivHTools":get_DivHTools(cliente.DivHTools),
            "dDivNextec":get_DivNextec(cliente.DivNextec),
            #"DireccioCliente":cliente.DireccioCliente,
            #"TelefonoPrincipal":cliente.TelefonoPrincipal,
            #"RFC":cliente.RFC,
            #"NombreAdicional":cliente.NombreAdicional,
            #"DivisionPM":cliente.DivisionPM,
    }
    return acliente

def editarCliente(request, usrid):
    IdCliente = request.POST['claveExterna']
    NombreCliente = request.POST['NombreCliente']
    #TipoCliente = request.POST['TipoCliente']
    ClientePotencial = request.POST['ClientePotencial']
    FechaNacimiento = request.POST['FechaNacimiento']
    Sector = request.POST['Sector']
    #ClientePotencial = request.POST['ClientePotencial']
    Estado = request.POST['Estado']
    #Duns = request.POST['Duns']
    #Clasificacion = request.POST['Clasificacion']
    #Division = request.POST['Division']
    #subDivision = request.POST['subDivision']
    #zonaServicio = request.POST['SucServicio']
    TipoEmpresa = request.POST['TipoEmpresa']
    #iDNielsen = request.POST['iDNielsen']
    #RegionVts = request.POST['RegionVts']
    NoTurnosC = request.POST['NoTurnosC']
    Tier = request.POST['Tier']
    #FrecuenciaCompra = request.POST['FrecuenciaCompra']
    #RegionVts = request.POST['RegionVts']
    NoMaqConvenC = request.POST['NoMaqConvenC']
    #NoMaqCNC_C = request.POST['NoMaqCNC_C']
    #NoMaqHT_C = request.POST['NoMaqHT_C']

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
        
    DivHaasMexico = DivHaasEcuador = DivHaasColombia = DivHaasCAM = False
    DivCNCCNC = DivCNCOmnitec = False
    DivHToolsTools = False
    #DivHToolsSolubles = False
    DivNextecFAB = DivNextecEDM = DivPMPM = False
    if "DivHaasMexico" in request.POST:
        DivHaasMexico = True
    if "DivHaasEcuador" in request.POST:
        DivHaasEcuador = True
    if "DivHaasColombia" in request.POST:
        DivHaasColombia = True
    if "DivHaasCAM" in request.POST:
        DivHaasCAM = True
    if "DivPM" in request.POST:
        DivPMPM = True
    if "DivHToolsTools" in request.POST:
        DivHToolsTools = True
    #if "DivHToolsSolubles" in request.POST:
    #    DivHToolsSolubles = True
    if "DivCNCCNC" in request.POST:
        DivCNCCNC = True
    if "DivCNCOmnitec" in request.POST:
        DivCNCOmnitec = True
    if "DivNextecEDM" in request.POST:
        DivNextecEDM = True
    if "DivNextecFAB" in request.POST:
        DivNextecFAB = True
    
    DivHaas   = getVal_DivHaas(DivHaasMexico, DivHaasEcuador, DivHaasColombia, DivHaasCAM)
    DivPM     = getVal_DivPM(DivPMPM)
    DivCNC    = getVal_DivCNC(DivCNCCNC, DivCNCOmnitec)
    DivHTools = getVal_DivHTools(DivHToolsTools, DivHToolsSolubles)
    DivNextec = getVal_DivNextec(DivNextecFAB, DivNextecEDM)
    

    #ActPriFAB = ActPriEDM = ActPriEquipoCNC = ""
    #ActPriEquipo = ""
    #if "ActPriFAB" in request.POST:
    #    ActPriFAB = request.POST['ActPriFAB']
    #if "ActPriEDM" in request.POST:
    #    ActPriEDM = request.POST['ActPriEDM']
    #if "ActPriEquipoCNC" in request.POST:
    #    ActPriEquipoCNC = request.POST['ActPriEquipoCNC']
    #if "ActPriEquipo" in request.POST:
        #ActPriEquipo = request.POST['ActPriEquipo']
    
    cliente = Clientes.objects.get(IdCliente=IdCliente)
    cliente.NombreCliente = NombreCliente
    cliente.FechaNacimiento = FechaNacimiento
    cliente.Sector = Sector
    #cliente.TipoCliente = TipoCliente
    #cliente.ClientePotencial = ClientePotencial
    cliente.Estado = Estado
    #cliente.Duns = Duns
    #cliente.Clasificacion = Clasificacion
    #cliente.Division = Division
    #cliente.subDivision = subDivision
    #cliente.SucServicio = zonaServicio
    cliente.TipoEmpresa = TipoEmpresa
    #cliente.iDNielsen= iDNielsen
    cliente.NoTurnosC = NoTurnosC
    cliente.Tier = Tier
    cliente.NoMaqConvenC = NoMaqConvenC
    #cliente.NoMaqCNC_C = NoMaqCNC_C
    #cliente.NoMaqHT_C = NoMaqHT_C
    cliente.MatUseCHMER = MatUseCHMER
    cliente.MatUseYIZUMI = MatUseYIZUMI
    cliente.MatUsoFab = MatUsoFab
    cliente.MatViruta = MatViruta
    #cliente.MatUsoCNC_Haas = MatUsoCNC_Haas
    #cliente.FrecuenciaCompra = FrecuenciaCompra
    #cliente.RegionVts = RegionVts
    #cliente.ActPriFAB = ActPriFAB
    #cliente.ActPriEDM = ActPriEDM
    #cliente.ActPriEquipoCNC = ActPriEquipoCNC
    #cliente.ActPriEquipo = ActPriEquipo
    cliente.DivHaas = DivHaas
    cliente.DivPM = DivPM
    cliente.DivCNC = DivCNC
    cliente.DivHTools = DivHTools
    cliente.DivNextec = DivNextec
    cliente.save()

    #Actualiza divisiones
    saveDivision(IdCliente, 1, 109, DivHaasMexico)
    saveDivision(IdCliente, 1, 111, DivHaasEcuador)
    saveDivision(IdCliente, 1, 112, DivHaasColombia)
    saveDivision(IdCliente, 1, 113, DivHaasCAM)
    saveDivision(IdCliente, 2, 116, DivPM)
    saveDivision(IdCliente, 3, 118, DivHToolsTools)
    #saveDivision(IdCliente, 3, 119, DivHToolsSolubles)
    saveDivision(IdCliente, 4, 121, DivCNCCNC)
    saveDivision(IdCliente, 4, 122, DivCNCOmnitec)
    saveDivision(IdCliente, 5, 123, DivNextecFAB)
    saveDivision(IdCliente, 5, 124, DivNextecEDM)

    data = {
        "NombreCliente": NombreCliente,
        "FechaNacimiento": FechaNacimiento,
        "Sector": Sector,
        #"TipoCliente": TipoCliente,
        #"ClientePotencial": ClientePotencial,
        "Estado": Estado,
        #"Duns": Duns,
        #"Clasificacion": Clasificacion,
        #"Division": Division,
        #"subDivision": subDivision,
        #"SucServicio": zonaServicio,
        "TipoEmpresa": TipoEmpresa,
        #"iDNielsen": iDNielsen,
        "NoTurnosC": NoTurnosC,
        "Tier": Tier,
        "NoMaqConvenC": NoMaqConvenC,
        #"NoMaqCNC_C": NoMaqCNC_C,
        #"NoMaqHT_C": NoMaqHT_C,
        "MatUseCHMER": MatUseCHMER,
        "MatUseYIZUMI": MatUseYIZUMI,
        "MatUsoFab": MatUsoFab,
        "MatViruta": MatViruta,
        #"MatUsoCNC_Haas": MatUsoCNC_Haas,
        #"FrecuenciaCompra": FrecuenciaCompra,
        #"RegionVts": RegionVts,
        #"ActPriFAB": ActPriFAB,
        #"ActPriEDM": ActPriEDM,
        #"ActPriEquipoCNC": ActPriEquipoCNC,
        #"ActPriEquipo": ActPriEquipo,
        "DivHaas": DivHaas,
        "DivPM": DivPM,
        "DivCNC": DivCNC,
        "DivHTools": DivHTools,
        "DivNextec": DivNextec,
        "DivHaasMexico": DivHaasMexico,
        "DivHaasEcuador": DivHaasEcuador,
        "DivHaasColombia": DivHaasColombia,
        "DivHaasCAM": DivHaasCAM,
        "DivPM": DivPM,
        "DivCNCCNC": DivCNCCNC,
        "DivCNCOmnitec": DivCNCOmnitec,
        "DivHToolsTools": DivHToolsTools,
        #"DivHToolsSolubles": DivHToolsSolubles,
        "DivNextecFAB": DivNextecFAB,
        "DivNextecEDM": DivNextecEDM,
    }

    addLog(usrid, "Update", "Clientes", IdCliente, data)
    messages.success(request, "Los datos del cliente fueron actualizados con éxito")
    return redirect('/edicionCliente/'+IdCliente+'/'+usrid)
    #return redirect('/home/'+usrid)

def gestionContactos(request, codigo, usrid):
    session = getSession(usrid)
    cliente = Clientes.objects.get(IdCliente=codigo)
    if Contactos.objects.filter(IdCliente=codigo).exists():
    # Si el cliente tiene contactos envía el listado de contactos del cliente
        contactosListados = Contactos.objects.all().filter(IdCliente=codigo)
        return render(request,"gestionContactos.html",{"contactos":contactosListados, "cliente":cliente, "session":session})
    else:
    # Si no hay contactos registrados, se envía agregar un contacto
        contacto = None
        flag1 = flag2 =False
        iniCodPos = ""
        iniDistrito = ""
        iniPais = {"CodeId":"MX", "Descrip":"México"}
        iniRegion = {"CodeId":"CMX", "Descrip":"Ciudad de México"}
        iniCheckbox = {"Principal":flag1, "VIP":flag2}
        descrip = getContactoDescrip("0", contacto)
        return render(request, "edicionContactos.html",{"vista":"Contacto", "Gestion":False, "idRegistro":"0", "contacto":contacto, "cliente":cliente, "session":session, "iniPais":iniPais, "iniRegion":iniRegion, "iniCodPos":iniCodPos, "iniDistrito":iniDistrito, "dataInt":False, "iniCheckbox":iniCheckbox, "descrip":descrip })

def edicionContacto(request, idCliente, codigo, Gestion, usrid):
    session = getSession(usrid)        
    cliente = Clientes.objects.get(IdCliente=idCliente)
    iniCodPos = ""
    iniDistrito = ""
    dataInt = False
    flag1 = flag2 = False
    if codigo=="0" :
        contacto = None
        iniPais = {"CodeId":"MX", "Descrip":"México"}
        iniRegion = {"CodeId":"CMX", "Descrip":"Ciudad de México"}
        iniMedioComunicacion = {"CodeId":"002", "Descrip":"Teléfono"}
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
    descrip = getContactoDescrip(codigo, contacto)
    
    return render(request, "edicionContactos.html",{"vista":"Contacto", "Gestion":Gestion, "idRegistro":codigo, "contacto":contacto, "cliente":cliente, "session":session, "logData":getLogData('Contactos', codigo), "iniPais":iniPais, "iniRegion":iniRegion, "iniCodPos":iniCodPos, "iniDistrito":iniDistrito, "dataInt":dataInt, "iniCheckbox":iniCheckbox, "descrip": descrip })

def getContactoDescrip(idContacto, contacto):
    dFuncion = dDepartamento = dMedioComunicacion = ""
    if(idContacto!="0"):
        dFuncion = get_Funcion(contacto.Funcion)
        dDepartamento = get_Departamento(contacto.Departamento)
        dMedioComunicacion = get_MedioComunicacion(contacto.MedioComunicacion)

    dContacto = {
        "dFuncion":         dFuncion,
        "dDepartamento":    dDepartamento,
        "dMedioComunicacion":dMedioComunicacion
    }
    return dContacto

def editarContacto(request, usrid):
    IdCliente = request.POST['IdCliente']
    IdContacto = request.POST['idRegistro']
    NombreContacto = request.POST['Nombre']
    SegundoNombre = request.POST['SegundoNombre']
    Apellidos = request.POST['Apellidos']
    Telefono = request.POST['Telefono']
    TelefonoMovil = request.POST['TelefonoMovil']
    CorreoElectronico = request.POST['CorreoElectronico']
    Departamento = Funcion = MedioComunicacion = ""

    if "Departamento" in request.POST:
        Departamento = request.POST['Departamento']
    if "Funcion" in request.POST:
        Funcion = request.POST['Funcion']
    if "MedioComunicacion" in request.POST:
        MedioComunicacion = request.POST['MedioComunicacion']

    #PaisRegion = request.POST['PaisRegion']
    #Estado = request.POST['Estado']

    #if (PaisRegion=="MX"):
    #    CodigoPostal = request.POST['CodigoPostal']
    #    Ciudad = request.POST['Ciudad']
    #    Distrito = request.POST['Distrito']
    #else :
    #    CodigoPostal = request.POST['IntCodigoPostal']
    #    Ciudad = request.POST['IntCiudad']
    #    Distrito = request.POST['IntDistrito']  

    #Calle = request.POST['Calle']
    #Numero = request.POST['Numero']
    #Edificio = request.POST['Edificio']
    #Planta = request.POST['Planta']
    #PaisExp = request.POST['PaisExp']
    
    Principal = Vip = 0
    
    if "Principal" in request.POST:
        Principal = 1    
    if 'VIP' in request.POST:
        Vip = 1

    if(IdContacto != "0") :
        movimiento = 'Update'
        contacto = Contactos.objects.get(IdContacto=IdContacto)
        contacto.Nombre = NombreContacto
        contacto.SegundoNombre = SegundoNombre
        contacto.Apellidos = Apellidos
        contacto.Telefono = Telefono
        contacto.TelefonoMovil = TelefonoMovil
        contacto.CorreoElectronico = CorreoElectronico
        contacto.Departamento = Departamento
        contacto.Funcion = Funcion
        contacto.MedioComunicacion = MedioComunicacion
        #contacto.PaisRegion = PaisRegion
        #contacto.Estado = Estado
        #contacto.CodigoPostal = CodigoPostal
        #contacto.Ciudad = Ciudad
        #contacto.Distrito = Distrito
        #contacto.Calle = Calle
        #contacto.Numero = Numero
        #contacto.Edificio = Edificio
        #contacto.Planta = Planta
        #contacto.PaisExp = PaisExp
        contacto.Principal = Principal
        contacto.Vip = Vip    
        contacto.save()
        messages.success(request, "Los datos del contacto fueron actualizados con éxito")

    else :
        movimiento = 'Create'
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
            MedioComunicacion = MedioComunicacion,
            #PaisRegion = PaisRegion,
            #Estado = Estado,
            #CodigoPostal = CodigoPostal,
            #Ciudad = Ciudad,
            #Distrito = Distrito,
            #Calle = Calle,
            #Numero = Numero,
            #Edificio = Edificio,
            #Planta = Planta,
            #PaisExp = PaisExp,
            Principal = Principal,
            Vip = Vip,
            Bloqueo = 0
        )
        IdContacto = contacto.IdContacto
        messages.success(request, "El contacto del cliente fue creado con éxito")
            
    data = { "IdContacto": IdContacto,
            "IdCliente": IdCliente,
            "Nombre": NombreContacto,
            "SegundoNombre": SegundoNombre,
            "Apellidos": Apellidos,
            "Telefono": Telefono,
            "TelefonoMovil": TelefonoMovil,
            "CorreoElectronico": CorreoElectronico,
            "Departamento": Departamento,
            "Funcion": Funcion,
            "MedioComunicacion": MedioComunicacion,
            #"PaisRegion": PaisRegion,
            #"Estado": Estado,
            #"CodigoPostal": CodigoPostal,
            #"Ciudad": Ciudad,
            #"Distrito": Distrito,
            #"Calle": Calle,
            #"Numero": Numero,
            #"Edificio": Edificio,
            #"Planta": Planta,
            #"PaisExp": PaisExp,
            "Principal": Principal,
            "Vip": Vip
    }

    entidad = "Contactos"
    addLog(usrid, movimiento, entidad, IdContacto, data)
    return redirect('/edicionContacto/'+IdCliente+'/'+IdContacto+'/Gestion/'+usrid)
    #return redirect("../gestionContactos/"+IdCliente+"/"+usrid)

def bloquearContacto(request, codigo,cliente, usrid):
    session = getSession(usrid)

    contacto = Contactos.objects.get(IdContacto=codigo)

    if contacto.Bloqueo != True:
        contacto.Bloqueo = True
        bloqueo = True
        messages.success(request, "El contacto del cliente ha sido Bloqueado")
    else:
        contacto.Bloqueo = False
        bloqueo = False
        messages.success(request, "El contacto del cliente ha sido Desbloqueado")

    contacto.save()
    
    addLog(usrid, "Bloqueo", "Contactos", codigo, {"Bloqueo":bloqueo})

    contactosListados = Contactos.objects.all().filter(IdCliente=cliente)
    return render(request,"gestionContactos.html",{"contactos":contactosListados, "cliente":cliente, "session":session})

def eliminarContacto(request,contacto,cliente):
    contacto = Contactos.objects.get(IdContacto=contacto)
    contacto.delete()
    contactosListados = Contactos.objects.all().filter(IdCliente=cliente)
    return render(request,"gestionContactos.html",{"contactos":contactosListados})

def setDirecciones(data):
    dPaisRegion = getDescripPais(data.PaisRegion)
    dRegion = getDescripPais(data.PaisRegion, data.Estado)

    aDirecciones = {
        "IdRegistro":data.IdRegistro, 
        "IdCliente": data.IdCliente,
        "PaisRegion": data.PaisRegion,
        "dPaisRegion": dPaisRegion,
        "Calle": data.Calle,
        "Numero": data.Numero,
        #"Calle2": data.Calle2,
        "Ciudad": data.Ciudad,
        "Estado": data.Estado,
        "dRegion": dRegion,
        "CodigoPostal": data.CodigoPostal,
        "Distrito": data.Distrito,
        "CodigoDomFiscal": data.CodigoDomFiscal,
        "DireccionPrincipal": data.DireccionPrincipal,
        "Entrega": data.Entrega,
        "DestinatarioMercEstandar": data.DestinatarioMercEstandar,
        "DestinatarioFactura": data.DestinatarioFactura,
        "Telefono": data.Telefono,
        "CorreoElectronico": data.CorreoElectronico,
        #"SitioWeb": data.SitioWeb,
        "Bloqueo": data.Bloqueo,
    }
    return aDirecciones

def gestionDirecciones(request,codigo, usrid):
    session = getSession(usrid) 
    cliente = Clientes.objects.get(IdCliente=codigo)
    if Direcciones.objects.filter(IdCliente=codigo).exists():
        direccionesListados = Direcciones.objects.all().filter(IdCliente=codigo)
        #direcciones = Direcciones.objects.all().filter(IdCliente=codigo)
        #for d in direcciones:
        #    direccionesListados = setDirecciones(d)
    # Si hay direcciones, se envía a gestión de direcciones
        return render(request,"gestionDirecciones.html",{"direcciones":direccionesListados, "cliente":cliente, "session":session})
    else:
    # Si no hay direcciones registradas, se envía a edicionClienteDireccion
        flag1 = flag2 = flag3 = flag4 = False
        iniCodPos = ""
        iniDistrito = ""
        iniPais = {"CodeId":"MX", "Descrip":"México"}
        iniRegion = {"CodeId":"CMX", "Descrip":"Ciudad de México"}
        iniCodDomFis = {"CodeId":"US", "Descrip":"Alabama"}
        iniCheckbox = {"DireccionPrincipal":flag1, "Entrega":flag2, "DestinatarioMercEstandar":flag3, "DestinatarioFactura":flag4}    
        
        return render(request,"edicionClienteDireccion.html",{"vista":"Cliente", "Gestion":False, "id":0, "cliente":cliente, "session":session, "iniPais":iniPais, "iniRegion":iniRegion, "iniCodPos":iniCodPos, "iniCodDomFis":iniCodDomFis, "iniDistrito":iniDistrito, "dataInt":False, "dataUS":False, "iniCheckbox":iniCheckbox})
    
def edicionClienteDireccion(request,idCliente, codigo, Gestion, usrid):
    session = getSession(usrid)
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
    return render(request, "edicionClienteDireccion.html",{"vista":"Cliente", "Gestion": Gestion, "id":codigo, "direcciones":direcciones, "cliente":cliente, "session":session, "logData":getLogData('Direcciones',codigo), "iniPais":iniPais, "iniRegion":iniRegion, "iniCodPos":iniCodPos, "iniCodDomFis":iniCodDomFis, "iniDistrito":iniDistrito, "dataInt":dataInt, "dataUS":dataUS, "iniCheckbox":iniCheckbox})

def editarDireccion(request, usrid):
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
    #Calle2 = request.POST['Calle2']
    CodigoDomFiscal = ""
    Telefono = request.POST['Telefono']
    CorreoElectronico = request.POST['CorreoElectronico']
    #SitioWeb = request.POST['SitioWeb']   

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
        movimiento = "Update"
        direcciones = Direcciones.objects.get(IdRegistro=idRegistro)
    
        direcciones.IdCliente = IdCliente
        direcciones.PaisRegion = PaisRegion
        direcciones.Calle = Calle
        direcciones.Numero = Numero
        #direcciones.Calle2 = Calle2
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
        #direcciones.SitioWeb =SitioWeb
        direcciones.save()
        messages.success(request, "Los datos de la dirección del Cliente fue actualizada con éxito")

    else :
        movimiento = "Create"
        #ultimo = Direcciones.objects.order_by('-IdRegistro').first()
        #idRegistro = ultimo.IdRegistro+1

        direcciones = Direcciones.objects.create (
            IdCliente = IdCliente,
            PaisRegion = PaisRegion,
            Calle = Calle,
            Numero = Numero,
            #Calle2 = Calle2,
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
            #SitioWeb =SitioWeb,
            Bloqueo = 0
        )
        idRegistro = direcciones.IdRegistro
        messages.success(request, "La dirección del Cliente fue creada con éxito")

    data = { 
            "IdCliente": IdCliente,
            "PaisRegion": PaisRegion,
            "Calle": Calle,
            "Numero": Numero,
            #"Calle2": Calle2,
            "Ciudad": Ciudad,
            "Estado": Estado,
            "CodigoPostal": CodigoPostal,
            "Distrito": Distrito,
            "CodigoDomFiscal": CodigoDomFiscal,
            "DireccionPrincipal": DireccionPrincipal,
            "Entrega": Entrega,
            "DestinatarioMercEstandar": DestinatarioMercEstandar,
            "DestinatarioFactura": DestinatarioFactura,
            "Telefono": Telefono,
            "CorreoElectronico": CorreoElectronico,
            #"SitioWeb": SitioWeb,
    }

    entidad = "Direcciones"
   
    addLog(usrid, movimiento, entidad, idRegistro, data)
    return redirect("/edicionClienteDireccion/"+IdCliente+"/"+str(idRegistro)+"/True/"+usrid)
    #return redirect("../gestionDirecciones/"+IdCliente+"/"+usrid)

def bloquearDireccion(request, cliente, idDireccion, usrid):
    session = getSession(usrid)

    direccion = Direcciones.objects.get(IdRegistro=idDireccion)

    if direccion.Bloqueo != True:
        direccion.Bloqueo = True
        bloqueo = True
        messages.success(request, "La dirección del cliente ha sido Bloqueada")
    else:
        direccion.Bloqueo = False
        bloqueo = False
        messages.success(request, "La dirección del cliente ha sido Desbloqueada")

    direccion.save()

    addLog(usrid, "Bloqueo", "Direcciones", idDireccion, {"Bloqueo":bloqueo})

    direccionesListados = Direcciones.objects.all().filter(IdCliente=cliente)
    cliente = Clientes.objects.get(IdCliente=cliente)
    return render(request,"gestionDirecciones.html",{"direcciones":direccionesListados, "cliente":cliente, "session":session})

def validDivision(IdCliente, IdDiv, IdSubDiv):
    if divisionCliente.objects.filter(IdContacto=IdCliente, IdDivision=IdDiv, IdSubdivision=IdSubDiv).exists():
        return True
    else:
        return False   

def saveDivision(IdCliente, IdDiv, IdSubDiv, save):
    if divisionCliente.objects.filter(IdContacto=IdCliente, IdDivision=IdDiv, IdSubdivision=IdSubDiv).exists():
        if(not save):
            registro = divisionCliente.objects.get(IdContacto=IdCliente, IdDivision=IdDiv, IdSubdivision=IdSubDiv)
            registro.delete()
            return
    else:
        if(save):
            division = divisionCliente.objects.create (
                IdContacto = IdCliente,
                IdDivision = IdDiv,
                IdSubdivision = IdSubDiv
            )
            return

#def agregarClienteDireccion(request,codigo):
#    return render(request,"agregarClienteDireccion.html",{"cliente":codigo})

def get_paises(request):
    paises = list(Country.objects.order_by('Descrip').values())
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
        #codigos = list(Sepomex.objects.annotate(cnt=Count('D_codigo')).filter(C_estado=c_estado).values('cnt', 'D_codigo').order_by('D_codigo'))
        codigos = list(Sepomex.objects.order_by().values_list('D_codigo', flat=True).values('D_codigo').distinct().filter(C_estado=c_estado))

    
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

def getDescripPais(request, codigo):
    descrip = ""
    if Country.objects.filter(CodeId=codigo).exists():
        pais = Country.objects.get(CodeId=codigo)
        descrip = pais.Descrip
    return descrip

def getDescripRegion(request, IdCountry, codigo):
    descrip = ""
    if Region.objects.filter(IdCountry=IdCountry, CodeId=codigo).exists():
        region = Region.objects.get(IdCountry=IdCountry, CodeId=codigo)
        descrip = region.Descrip
    return descrip

def get_Sector(codigo):
    descrip = ""
    if (codigo == 'Z01') :        descrip = 'Aeroespacial y Aeronáutica'
    elif (codigo == '11') :       descrip = 'Agrícola'
    elif (codigo == 'Z02') :      descrip = 'Alimentos y bebidas'
    elif (codigo == 'Z04') :      descrip = 'Automotriz'
    elif (codigo == 'Z06') :      descrip = 'Bombas y válvulas'
    elif (codigo == 'Z08') :      descrip = 'Calzado'
    elif (codigo == '23') :       descrip = 'Construcción'
    elif (codigo == 'Z11') :      descrip = 'Educación'
    elif (codigo == 'Z12') :      descrip = 'Eléctrico/Electrónica'
    elif (codigo == 'Z13') :      descrip = 'Entretenimiento y Deportes'
    elif (codigo == 'Z14') :      descrip = 'Estructuras y Perfiles'
    elif (codigo == 'Z15') :      descrip = 'Farmacéutico'
    elif (codigo == 'Z16') :      descrip = 'Ferrocarril'
    elif (codigo == 'Z17') :      descrip = 'Forja'
    elif (codigo == 'Z18') :      descrip = 'Fundición'
    elif (codigo == 'Z19') :      descrip = 'Generación de Energía'
    elif (codigo == 'Z20') :      descrip = 'Gobierno'
    elif (codigo == 'Z21') :      descrip = 'Herramientas y utillaje'
    elif (codigo == 'Z22') :      descrip = 'Instrumental de precisión'
    elif (codigo == 'Z23') :      descrip = 'Joyería'
    elif (codigo == 'Z24') :      descrip = 'Línea blanca'
    elif (codigo == 'Z25') :      descrip = 'Mantenimiento'
    elif (codigo == 'Z26') :      descrip = 'Médico / Dental'
    elif (codigo == 'Z27') :      descrip = 'Militar'
    elif (codigo == 'Z28') :      descrip = 'Minera'
    elif (codigo == 'Z29') :      descrip = 'Moldes, troqueles y matrices'
    elif (codigo == 'Z30') :      descrip = 'Muebles'
    elif (codigo == 'Z31') :      descrip = 'Naval'
    elif (codigo == 'Z33') :      descrip = 'Otras'
    elif (codigo == 'Z34') :      descrip = 'Papelero'
    elif (codigo == 'Z35') :      descrip = 'Petróleo y gas'
    elif (codigo == 'Z39') :      descrip = 'Robótica y automatización'
    elif (codigo == 'Z40') :      descrip = 'Textil'

    #if(codigo=="11"):            descrip = "Agrícola" 
    #elif (codigo == '22') :      descrip = 'Servicios públicos'
    #elif (codigo == '23') :      descrip = 'Construcción'
    #elif (codigo == '31') :      descrip = 'Fabricación'
    #elif (codigo == '42') :      descrip = 'Comercio mayorista'
    #elif (codigo == '44') :      descrip = 'Comercio minorista'
    #elif (codigo == '48') :      descrip = 'Transporte y almacenamiento'
    #elif (codigo == '51') :      descrip = 'Información'
    #elif (codigo == '52') :      descrip = 'Finanzas y seguro'
    #elif (codigo == '53') :      descrip = 'Bienes inmuebles, alquiler y leasing'
    #elif (codigo == '54') :      descrip = 'Servicios profesionales, científicos y técnicos'
    #elif (codigo == '55') :      descrip = 'Gestión de compañías y empresas'
    #elif (codigo == '56') :      descrip = 'Servicios de recuperación, gestión de desechos y soporte administrativo'
    #elif (codigo == '61') :      descrip = 'Servicios educativos'
    #elif (codigo == '62') :      descrip = 'Atención médica y asistencia social'
    #elif (codigo == '71') :      descrip = 'Arte, entretenimiento y recreación'
    #elif (codigo == '72') :      descrip = 'Servicios de alimentación y alojamiento'
    #elif (codigo == '81') :      descrip = 'Otros servicios (excepto administración pública)'
    #elif (codigo == '92') :      descrip = 'Administración pública'
    #elif (codigo == 'Z01') :      descrip = 'Aeroespacial y Aeronáutica'
    #elif (codigo == 'Z02') :      descrip = 'Alimentos y bebidas'
    #elif (codigo == 'Z03') :      descrip = 'Artículos y Maquinaria Industrial'
    #elif (codigo == 'Z04') :      descrip = 'Automotriz'
    #elif (codigo == 'Z05') :      descrip = 'Bearings'
    #elif (codigo == 'Z06') :      descrip = 'Bombas y válvulas otras'
    #elif (codigo == 'Z07') :      descrip = 'Bombas y válvulas PET'
    #elif (codigo == 'Z08') :      descrip = 'Calzado'
    #elif (codigo == 'Z10') :      descrip = 'Corte lámina'
    #elif (codigo == 'Z11') :      descrip = 'Educación'
    #elif (codigo == 'Z12') :      descrip = 'Eléctrico'
    #elif (codigo == 'Z13') :      descrip = 'Entretenimiento y Deportes'
    #elif (codigo == 'Z14') :      descrip = 'Estructuras y Perfiles'
    #elif (codigo == 'Z15') :      descrip = 'Farmacéutico'
    #elif (codigo == 'Z16') :      descrip = 'Ferrocarril'
    #elif (codigo == 'Z17') :      descrip = 'Forja'
    #elif (codigo == 'Z18') :      descrip = 'Funcición'
    #elif (codigo == 'Z19') :      descrip = 'Generación de Energía'
    #elif (codigo == 'Z20') :      descrip = 'Gobierno'
    #elif (codigo == 'Z21') :      descrip = 'Herramientas y utillaje'
    #elif (codigo == 'Z22') :      descrip = 'Instrumental de precisión'
    #elif (codigo == 'Z23') :      descrip = 'Joyería'
    #elif (codigo == 'Z24') :      descrip = 'Línea blanca'
    #elif (codigo == 'Z25') :      descrip = 'Mantenimiento'
    #elif (codigo == 'Z26') :      descrip = 'Médico'
    #elif (codigo == 'Z27') :      descrip = 'Militar'
    #elif (codigo == 'Z28') :      descrip = 'Minera'
    #elif (codigo == 'Z29') :      descrip = 'Moldes, troqueles y matrices'
    #elif (codigo == 'Z30') :      descrip = 'Muebles'
    #elif (codigo == 'Z31') :      descrip = 'Naval'
    #elif (codigo == 'Z33') :      descrip = 'Otras'
    #elif (codigo == 'Z34') :      descrip = 'Papelelero'
    #elif (codigo == 'Z35') :      descrip = 'Petróleo y Gas'
    #elif (codigo == 'Z36') :      descrip = 'Plástico'
    #elif (codigo == 'Z37') :      descrip = 'Prensado'
    #elif (codigo == 'Z38') :      descrip = 'Químico'
    #elif (codigo == 'Z39') :      descrip = 'Robótica y automatización'
    #elif (codigo == 'Z40') :      descrip = 'Textil'
    #elif (codigo == 'Z41') :      descrip = 'Taller/Maquiladora'
    else :                        descrip = ""

    return (descrip)

def get_ClientePotencial(codigo) :
    if (codigo == True) :   descrip = 'Si'
    else :                  descrip = 'No'

    return (descrip)

def get_Estado(codigo) :
    if (codigo == True) :   descrip = 'Activo'
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

def get_RegionVts2(codigo) :
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

def get_Funcion(codigo) :
    descrip = ""
    if   (codigo == '01') :      descrip = 'Administrador'
    elif (codigo == '02') :      descrip = 'Analista'
    elif (codigo == '03') :      descrip = 'Arquitecto'
    elif (codigo == '04') :      descrip = 'Asistente'
    elif (codigo == '05') :      descrip = 'Auxiliar'
    elif (codigo == '06') :      descrip = 'Contador'
    elif (codigo == '07') :      descrip = 'Coordinador'
    elif (codigo == '08') :      descrip = 'Desarrollador'
    elif (codigo == '09') :      descrip = 'Director'
    elif (codigo == '10') :      descrip = 'Diseñador'
    elif (codigo == '11') :      descrip = 'Encargado Almacén/Logística'
    elif (codigo == '12') :      descrip = 'Estudiante'
    elif (codigo == '13') :      descrip = 'Gerente'
    elif (codigo == '14') :      descrip = 'Ingeniero'
    elif (codigo == '15') :      descrip = 'Jefe'
    elif (codigo == '16') :      descrip = 'Operador'
    elif (codigo == '17') :      descrip = 'Programador'
    elif (codigo == '18') :      descrip = 'Propietario'
    elif (codigo == '19') :      descrip = 'Supervisor'
    elif (codigo == '20') :      descrip = 'Técnico'
    elif (codigo == '21') :      descrip = 'Vendedor'
    return (descrip)

def get_Departamento(codigo) :
    descrip = ""
    if   (codigo == '01') :      descrip = 'Administración'
    elif (codigo == '02') :      descrip = 'Almacén'
    elif (codigo == '03') :      descrip = 'Compras'
    elif (codigo == '04') :      descrip = 'Diseño'
    elif (codigo == '05') :      descrip = 'Finanzas'
    elif (codigo == '06') :      descrip = 'Logística'
    elif (codigo == '07') :      descrip = 'Mantenimiento'
    elif (codigo == '08') :      descrip = 'Marketing'
    elif (codigo == '09') :      descrip = 'Producción'
    elif (codigo == '10') :      descrip = 'Recursos Humanos'
    elif (codigo == '11') :      descrip = 'Servicio al Cliente'
    elif (codigo == '12') :      descrip = 'Servicio Técnico'
    elif (codigo == '13') :      descrip = 'TI'
    elif (codigo == '14') :      descrip = 'Ventas'
    return (descrip)

def get_FuncionOld(codigo) :
    descrip = ""
    if   (codigo == 'Z001') :      descrip = 'Arrento'
    elif (codigo == 'Z002') :      descrip = 'Fnto'
    elif (codigo == 'Z003') :      descrip = 'Tec'
    elif (codigo == 'Z004') :      descrip = 'Ent'
    elif (codigo == 'Z005') :      descrip = 'Comp'
    elif (codigo == 'Z006') :      descrip = 'Fact'
    elif (codigo == 'Z007') :      descrip = 'CxP'
    elif (codigo == 'Z008') :      descrip = 'Tec y Fnto'
    elif (codigo == 'Z009') :      descrip = 'Tec y Arrento'
    elif (codigo == 'Z010') :      descrip = 'Tec y Ent'
    elif (codigo == 'Z011') :      descrip = 'Tec y Comp'
    elif (codigo == 'Z012') :      descrip = 'Tec y Fact'
    elif (codigo == 'Z013') :      descrip = 'Comp y Fact'
    elif (codigo == 'Z014') :      descrip = 'Comp y Ent'
    elif (codigo == 'Z015') :      descrip = 'Arrento y Fact'
    elif (codigo == 'Z016') :      descrip = 'Arrento y Ent'
    elif (codigo == 'Z017') :      descrip = 'Fnto y Fact'
    elif (codigo == 'Z018') :      descrip = 'Fnto y Ent'
    elif (codigo == 'Z019') :      descrip = 'Ent y Fact'
    elif (codigo == 'Z020') :      descrip = 'Tec Comp y Ent'
    elif (codigo == 'Z021') :      descrip = 'Tec Comp y Fact'
    elif (codigo == 'Z022') :      descrip = 'Tec Ent y Fact'
    elif (codigo == 'Z023') :      descrip = 'Arrento Comp y Ent'
    elif (codigo == 'Z024') :      descrip = 'Arrento Comp y Fact'
    elif (codigo == 'Z025') :      descrip = 'Arrento Ent y Fact'
    elif (codigo == 'Z026') :      descrip = 'Arrento Ent y Tec'
    elif (codigo == 'Z027') :      descrip = 'Fnto Comp y Fact'
    elif (codigo == 'Z028') :      descrip = 'Fnto Comp y Ent'
    elif (codigo == 'Z029') :      descrip = 'Fnto Ent y Fact'
    elif (codigo == 'Z030') :      descrip = 'Fnto Ent y Tec'
    elif (codigo == 'Z031') :      descrip = 'Comp Ent y Fact'
    elif (codigo == 'Z032') :      descrip = 'Comp Ent y Tec'
    elif (codigo == 'Z033') :      descrip = 'Comp Fact y Tec'
    elif (codigo == 'Z034') :      descrip = 'Tec Comp Ent Fact'
    elif (codigo == 'Z035') :      descrip = 'Tec Comp Ent Fact y Arrento'
    elif (codigo == 'Z036') :      descrip = 'Tec Comp Ent Fact y Fnto'
    elif (codigo == 'Z037') :      descrip = 'Fnto Comp Ent y Fact'
    elif (codigo == 'Z038') :      descrip = 'Arrento Comp Ent y Fact'

    return (descrip)

def get_DepartamentoOld(codigo) :
    descrip = ""
    if   (codigo == '0001') :      descrip = 'Dep.compras'
    elif (codigo == '0002') :      descrip = 'Dep.ventas'
    elif (codigo == '0003') :      descrip = 'Dep.administración'
    elif (codigo == '0004') :      descrip = 'Dep.producción'
    elif (codigo == '0005') :      descrip = 'Dep.gestión calidad'
    elif (codigo == '0006') :      descrip = 'Secretaría'
    elif (codigo == '0007') :      descrip = 'Dep.financiero'
    elif (codigo == '0008') :      descrip = 'Dep.jurídico'
    elif (codigo == '0009') :      descrip = 'Dep.Recursos Humanos'
    elif (codigo == '0010') :      descrip = 'Dep.asuntos gen.'
    elif (codigo == '0011') :      descrip = 'Dep.promoción'
    elif (codigo == '0012') :      descrip = 'Dep.internacional'
    elif (codigo == '0013') :      descrip = 'Dep.exportación'
    elif (codigo == '0014') :      descrip = 'Dep.importación'
    elif (codigo == '0015') :      descrip = 'Dep.rel.públicas'
    elif (codigo == '0016') :      descrip = 'Dep.publicidad'
    elif (codigo == '0017') :      descrip = 'Dep.planificación'
    elif (codigo == '0018') :      descrip = 'Dep.invest.desar.'
    elif (codigo == '0019') :      descrip = 'Dep.Desarr.product.'
    elif (codigo == '0020') :      descrip = 'Oficina comercial'
    elif (codigo == '0021') :      descrip = 'Dep.servicio'
    elif (codigo == '0022') :      descrip = 'Soporte técnico'
    elif (codigo == '0023') :      descrip = 'Departamento de TI'
    elif (codigo == '0024') :      descrip = 'Departam.Logística'

    return (descrip)

def getVal_DivHaas(divMexico, divEcuador, divColombia, divCAM) :
    codigo = ""
    if   (divMexico):   codigo = '109'
    elif (divEcuador):  codigo = '111'
    elif (divColombia): codigo = '112'
    elif (divCAM):      codigo = '113'
    return (codigo)

def getVal_DivPM(divPM) :
    codigo = ""
    if   (divPM):       codigo = '116'
    return (codigo)

def getVal_DivHTools(divTools, divSolubles) :
    codigo = ""
    if   (divTools):    codigo = '118'
    elif (divSolubles): codigo = '119'
    return (codigo)

def getVal_DivCNC(divCNC, divOmnitec) :
    codigo = ""
    if   (divCNC):      codigo = '121'
    elif (divOmnitec):  codigo = '122'
    return (codigo)

def getVal_DivNextec(divFAB, divEDM) :
    codigo = ""
    if   (divFAB):      codigo = '123'
    elif (divEDM):      codigo = '124'
    return (codigo)

def getCodigo_DivHaas(division) :
    codigo = ""
    if   (division == 'DivHaasMexico'):     codigo = '109'
    elif (division == 'DivHaasEcuador'):    codigo = '111'
    elif (division == 'DivHaasColombia'):   codigo = '112'
    elif (division == 'DivHaasCAM'):        codigo = '113'
    elif (division == 'DivHaasEspana'):     codigo = '114'
    return (codigo)

def getCodigo_DivPM(division) :
    codigo = ""
    if   (division == 'DivPMPM'):           codigo = '116'
    return (codigo)

def getCodigo_DivHTools(division) :
    codigo = ""
    if   (division == 'DivHToolsTools'):    codigo = '118'
    elif (division == 'DivHToolsSolubles'): codigo = '119'
    return (codigo)

def getCodigo_DivCNC(division) :
    codigo = ""
    if   (division == 'DivCNCCNC'):     codigo = '121'
    elif (division == 'DivCNCOmnitec'): codigo = '122'
    return (codigo)

def getCodigo_DivNextec(division) :
    codigo = ""
    if   (division == 'DivNextecFAB'):  codigo = '123'
    elif (division == 'DivNextecEDM'):  codigo = '124'
    return (codigo)

def get_DivHaas(codigo) :
    descrip = ""
    if   (codigo == '109') :      descrip = 'HFO MEXICO'
    elif (codigo == '111') :      descrip = 'HFO ECUADOR'
    elif (codigo == '112') :      descrip = 'HFO COLOMBIA'
    elif (codigo == '113') :      descrip = 'HFO CAM'
    elif (codigo == '114') :      descrip = 'HFO ESPAÑA'    
    return (descrip)

def get_DivPM(codigo) :
    descrip = ""
    if   (codigo == '116') :      descrip = 'PM'    
    return (descrip)

def get_DivHTools(codigo) :
    descrip = ""
    if   (codigo == '118') :      descrip = 'TOOLS'
    elif (codigo == '119') :      descrip = 'SOLUBLES'    
    return (descrip)

def get_DivCNC(codigo) :
    descrip = ""
    if   (codigo == '121') :      descrip = 'CNC'
    elif (codigo == '122') :      descrip = 'OMNITEC'
    return (descrip)

def get_DivNextec(codigo) :
    descrip = ""
    if   (codigo == '123') :      descrip = 'FAB'
    elif (codigo == '124') :      descrip = 'EDM'    
    return (descrip)

def get_MedioComunicacion(codigo) :
    descrip = ""
    if   (codigo == '001') :      descrip = 'Mail'
    elif (codigo == '002') :      descrip = 'Teléfono'
    elif (codigo == '003') :      descrip = 'WhatsApp'
    return (descrip)

def buscarCliente(request, usrid):
    session = getSession(usrid)
    busqueda = request.POST['Busqueda']
    clientes = Clientes.objects.all()[0:200]

    if busqueda:
        clientes = Clientes.objects.filter(
            Q(IdCliente__icontains = busqueda) |
            Q(NombreCliente__icontains = busqueda) |
            Q(RFC__icontains = busqueda) |
            Q(Duns__icontains = busqueda) 
        ).distinct()
        clientesOk = []
        for item in clientes.iterator():
            item.RegionVts = get_RegionVts(item.RegionVts)
            clientesOk.append(item)

    return render(request, "gestionClientesBusqueda.html",{"clientes":clientesOk, "session":session})

def addLog(usrid, movimiento, entidad, id, data) :
    fecha = datetime.now()
    logdata = Log.objects.create (
        Fecha = fecha,
        IdUser = usrid,
        Entidad = entidad,
        IdEnt = id,
        TipoMov = movimiento,
        Movimiento = movimiento,
        Movimientojson = data
    )

    return True

def getLogData(entidad, idRegistro):
    cant = 0
    fecha = datetime.today()
    user = ""

    if(idRegistro!="0"):
        if Log.objects.filter(Entidad=entidad, IdEnt=idRegistro).exists():
            cant = Log.objects.filter(Entidad=entidad, IdEnt=idRegistro).count()
            ultimo = Log.objects.filter(Entidad=entidad, IdEnt=idRegistro).order_by('-id').first()
            idusr = ultimo.IdUser
            fecha = ultimo.Fecha
            usuario = Users.objects.get(Id=idusr)
            user = usuario.Nombre

    logData = {
        "cant":  cant,
        "user":  user,
        "fecha": fecha
    }
    return logData
