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
    #clientes = Clientes.objects.all().filter(IdUser=usrid)[0:200]
    clientes = Clientes.objects.all().filter()[0:200]
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
            #clientes = Clientes.objects.all().filter(IdUser=usrid)[0:200]
            clientes = Clientes.objects.all().filter()[0:200]
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
    division = setDivisionCliente(cliente)
    material = getMaterialesCliente(codigo)
    maquinas = getMaquinasCliente(cliente)
    
    return render(request, "edicionCliente.html",{"cliente":acliente, "division":division, "material":material, "maquinas":maquinas, "session":session, "logData":getLogData('Clientes', codigo)})

def setDivisionCliente(cliente):
    DivHaasMexico = validDivision(cliente.IdCliente, 1, 109)
    #DivHaasEcuador = validDivision(cliente.IdCliente, 1, 111)
    #DivHaasColombia = validDivision(cliente.IdCliente, 1, 112)
    #DivHaasCAM = validDivision(cliente.IdCliente, 1, 113)
    DivPM = validDivision(cliente.IdCliente, 2, 116)
    DivHToolsTools = validDivision(cliente.IdCliente, 3, 118)
    #DivHToolsSolubles = validDivision(cliente.IdCliente, 3, 119)
    DivCNCCNC = validDivision(cliente.IdCliente, 4, 121)
    DivCNCOmnitec = validDivision(cliente.IdCliente, 4, 122)
    DivNextecFAB = validDivision(cliente.IdCliente, 5, 123)
    DivNextecEDM = validDivision(cliente.IdCliente, 5, 124)

    division = {
        "DivHaasMexico":DivHaasMexico,
        #"DivHaasEcuador":DivHaasEcuador,
        #"DivHaasColombia":DivHaasColombia,
        #"DivHaasCAM":DivHaasCAM,
        "DivPM":DivPM,
        "DivCNCCNC":DivCNCCNC,
        "DivCNCOmnitec":DivCNCOmnitec,
        "DivHToolsTools":DivHToolsTools,
        #"DivHToolsSolubles":DivHToolsSolubles,
        "DivNextecFAB":DivNextecFAB,
        "DivNextecEDM":DivNextecEDM,
    }
    return division

def getMaterialesCliente(codigo):
    ArrVirMat01 = ArrVirMat02 = ArrVirMat03 = ArrVirMat04 = ArrVirMat05 = ArrVirMat06 = False
    ElectroMat01 = ElectroMat02 = ElectroMat03 = ElectroMat04 = ElectroMat05 = ElectroMat06 = ElectroMat07 = False
    InyecMat01 = InyecMat02 = InyecMat03 = InyecMat04 = InyecMat05 = InyecMat06 = InyecMat07 = False
    FABMat01 = FABMat02 = FABMat03 = FABMat04 = FABMat05 = False

    if MaterialCliente.objects.filter(IdCliente=codigo).exists():
        data = MaterialCliente.objects.all().filter(IdCliente=codigo)
        for item in data.iterator():
            if (item.IdMaterial=="01"):
                #Arranque de Viruta
                if  (item.IdTipo=="163"):
                    ArrVirMat01 = True
                elif(item.IdTipo=="164"):
                    ArrVirMat02 = True
                elif(item.IdTipo=="165"):
                    ArrVirMat03 = True
                elif(item.IdTipo=="166"):
                    ArrVirMat04 = True
                elif(item.IdTipo=="167"):
                    ArrVirMat05 = True
                elif(item.IdTipo=="168"):
                    ArrVirMat06 = True
            elif (item.IdMaterial=="02"):
                #Electroerosión
                if  (item.IdTipo=="170"):
                    ElectroMat01 = True
                elif(item.IdTipo=="171"):
                    ElectroMat02 = True
                elif(item.IdTipo=="172"):
                    ElectroMat03 = True
                elif(item.IdTipo=="173"):
                    ElectroMat04 = True
                elif(item.IdTipo=="174"):
                    ElectroMat05 = True
                elif(item.IdTipo=="175"):
                    ElectroMat06 = True
                elif(item.IdTipo=="176"):
                    ElectroMat07 = True
            elif (item.IdMaterial=="03"):
                #Inyección
                if  (item.IdTipo=="179"):
                    InyecMat01 = True
                elif(item.IdTipo=="180"):
                    InyecMat02 = True
                elif(item.IdTipo=="181"):
                    InyecMat03 = True
                elif(item.IdTipo=="182"):
                    InyecMat04 = True
                elif(item.IdTipo=="183"):
                    InyecMat05 = True
                elif(item.IdTipo=="184"):
                    InyecMat06 = True
                elif(item.IdTipo=="185"):
                    InyecMat07 = True
            elif (item.IdMaterial=="04"):
                # FAB
                if  (item.IdTipo=="187"):
                    FABMat01 = True
                elif(item.IdTipo=="188"):
                    FABMat02 = True
                elif(item.IdTipo=="189"):
                    FABMat03 = True
                elif(item.IdTipo=="190"):
                    FABMat04 = True
                elif(item.IdTipo=="191"):
                    FABMat05 = True
                    
    datos = {
        "ArrVirMat01": ArrVirMat01,
        "ArrVirMat02": ArrVirMat02,
        "ArrVirMat03": ArrVirMat03,
        "ArrVirMat04": ArrVirMat04,
        "ArrVirMat05": ArrVirMat05,
        "ArrVirMat06": ArrVirMat06,
        "ElectroMat01": ElectroMat01,
        "ElectroMat02": ElectroMat02,
        "ElectroMat03": ElectroMat03,
        "ElectroMat04": ElectroMat04,
        "ElectroMat05": ElectroMat05,
        "ElectroMat06": ElectroMat06,
        "ElectroMat07": ElectroMat07,
        "InyecMat01": InyecMat01,
        "InyecMat02": InyecMat02,
        "InyecMat03": InyecMat03,
        "InyecMat04": InyecMat04,
        "InyecMat05": InyecMat05,
        "InyecMat06": InyecMat06,
        "InyecMat07": InyecMat07,
        "FABMat01": FABMat01,
        "FABMat02": FABMat02,
        "FABMat03": FABMat03,
        "FABMat04": FABMat04,
        "FABMat05": FABMat05,
    }

    return datos

def getMaquinasCliente(cliente):
    MarcaArrVir01 = "Dn Solutions"
    MarcaArrVir02 = 'Okuma'
    MarcaArrVir03 = 'Dmg Mori'
    MarcaArrVir04 = 'Mazak'
    MarcaArrVir05 = 'Hision'
    MarcaArrVir06 = 'Hyundai'
    MarcaArrVir07 = 'Baoji'
    MarcaArrVir08 = 'Makino'
    MarcaArrVir09 = 'Romi'
    MarcaArrVir10 = 'Chiron'
    MarcaArrVirOtra = getMarca(cliente.IdCliente, '01', 'Otr')

    MarcaElectro01 = "Sodick"
    MarcaElectro02 = 'Mitsubishi'
    MarcaElectro03 = 'Shem'
    MarcaElectro04 = 'Accutex'
    MarcaElectro05 = 'Makino'
    MarcaElectro06 = 'Ipretech'
    MarcaElectro07 = 'Mc-Lane'
    MarcaElectro08 = 'Excetek'
    MarcaElectro09 = 'Maincasa'
    MarcaElectro10 = 'Protecnic'
    MarcaElectroOtra = getMarca(cliente.IdCliente, '02', 'Otr')
    
    MarcaInyec01 = "Haitian"
    MarcaInyec02 = 'Engel'
    MarcaInyec03 = 'Sumitomo'
    MarcaInyec04 = 'Krauss Maffei'
    MarcaInyec05 = 'Nissei'
    MarcaInyec06 = 'Borche'
    MarcaInyec07 = 'Arburg'
    MarcaInyec08 = 'CLF'
    MarcaInyec09 = 'Tai-Mex'
    MarcaInyec10 = 'Bole'
    MarcaInyecOtra = getMarca(cliente.IdCliente, '03', 'Otr')
    
    MarcaLaser01 = "Bodor"
    MarcaLaser02 = 'Gweike'
    MarcaLaser03 = 'Trumpf'
    MarcaLaser04 = 'Bimex'
    MarcaLaser05 = 'Durma'
    MarcaLaser06 = 'Aida'
    MarcaLaser07 = 'Amada'
    MarcaLaser08 = 'JFY'
    MarcaLaser09 = 'Bystronic'
    MarcaLaser10 = 'BLM'
    MarcaLaserOtra = getMarca(cliente.IdCliente, '04', 'Otr')
    
    MarcaPrensa01 = "Fagor"
    MarcaPrensa02 = 'Aida'
    MarcaPrensa03 = 'Simpac'
    MarcaPrensa04 = 'Shem'
    MarcaPrensa05 = 'Amada'
    MarcaPrensa06 = 'Komatsu'
    MarcaPrensa07 = 'Schuler'
    MarcaPrensa08 = 'Marubeni'
    MarcaPrensa09 = 'Mitsubishi'
    MarcaPrensa10 = 'Seyi'
    MarcaPrensaOtra = getMarca(cliente.IdCliente, '05', 'Otr')
    
    MarcaDoblad01 = "Durma"
    MarcaDoblad02 = 'Amada'
    MarcaDoblad03 = 'Shem'
    MarcaDoblad04 = 'Bystronic'
    MarcaDoblad05 = 'Yawe'
    MarcaDoblad06 = 'Amob'
    MarcaDoblad07 = 'Trumpf'
    MarcaDoblad08 = 'BLM'
    MarcaDoblad09 = 'Nargesa'
    MarcaDoblad10 = 'MVD'
    MarcaDobladOtra = getMarca(cliente.IdCliente, '06', 'Otr')
    
    ArrVirMarca01 = ArrVirMarca02 = ArrVirMarca03 = ArrVirMarca04 = ArrVirMarca05 = ArrVirMarca06 = ArrVirMarca07 = ArrVirMarca08 = ArrVirMarca09 = ArrVirMarca10 = ArrVirMarcaOtra = False
    ElectroMarca01 = ElectroMarca02 = ElectroMarca03 = ElectroMarca04 = ElectroMarca05 = ElectroMarca06 = ElectroMarca07 = ElectroMarca08 = ElectroMarca09 = ElectroMarca10 = ElectroMarcaOtra = False
    InyecMarca01 = InyecMarca02 = InyecMarca03 = InyecMarca04 = InyecMarca05 = InyecMarca06 = InyecMarca07 = InyecMarca08 = InyecMarca09 = InyecMarca10 = InyecMarcaOtra = False
    LaserMarca01 = LaserMarca02 = LaserMarca03 = LaserMarca04 = LaserMarca05 = LaserMarca06 = LaserMarca07 = LaserMarca08 = LaserMarca09 = LaserMarca10 = LaserMarcaOtra = False
    PrensaMarca01 = PrensaMarca02 = PrensaMarca03 = PrensaMarca04 = PrensaMarca05 = PrensaMarca06 = PrensaMarca07 = PrensaMarca08 = PrensaMarca09 = PrensaMarca10 = PrensaMarcaOtra = False
    DobladMarca01 = DobladMarca02 = DobladMarca03 = DobladMarca04 = DobladMarca05 = DobladMarca06 = DobladMarca07 = DobladMarca08 = DobladMarca09 = DobladMarca10 = DobladMarcaOtra = False

    if MaquinasCliente.objects.filter(IdCliente=cliente.IdCliente).exists():
        data = MaquinasCliente.objects.all().filter(IdCliente=cliente.IdCliente)
        for item in data.iterator():
            if   ( item.IdMaquina == '01'):
                if  ( item.IdMarca == '01'):
                    ArrVirMarca01 = True
                elif( item.IdMarca == '02'):
                    ArrVirMarca02 = True
                elif( item.IdMarca == '03'):
                    ArrVirMarca03 = True
                elif( item.IdMarca == '04'):
                    ArrVirMarca04 = True
                elif( item.IdMarca == '05'):
                    ArrVirMarca05 = True
                elif( item.IdMarca == '06'):
                    ArrVirMarca06 = True
                elif( item.IdMarca == '07'):
                    ArrVirMarca07 = True
                elif( item.IdMarca == '08'):
                    ArrVirMarca08 = True
                elif( item.IdMarca == '09'):
                    ArrVirMarca09 = True
                elif( item.IdMarca == '10'):
                    ArrVirMarca10 = True
                elif( item.IdMarca == 'Otr'):
                    ArrVirMarcaOtra = True
            elif ( item.IdMaquina == '02'):
                if  ( item.IdMarca == '01'):
                    ElectroMarca01 = True
                elif( item.IdMarca == '02'):
                    ElectroMarca02 = True
                elif( item.IdMarca == '03'):
                    ElectroMarca03 = True
                elif( item.IdMarca == '04'):
                    ElectroMarca04 = True
                elif( item.IdMarca == '05'):
                    ElectroMarca05 = True
                elif( item.IdMarca == '06'):
                    ElectroMarca06 = True
                elif( item.IdMarca == '07'):
                    ElectroMarca07 = True
                elif( item.IdMarca == '08'):
                    ElectroMarca08 = True
                elif( item.IdMarca == '09'):
                    ElectroMarca09 = True
                elif( item.IdMarca == '10'):
                    ElectroMarca10 = True
                elif( item.IdMarca == 'Otr'):
                    ElectroMarcaOtra = True
            elif ( item.IdMaquina == '03'):
                if  ( item.IdMarca == '01'):
                    InyecMarca01 = True
                elif( item.IdMarca == '02'):
                    InyecMarca02 = True
                elif( item.IdMarca == '03'):
                    InyecMarca03 = True
                elif( item.IdMarca == '04'):
                    InyecMarca04 = True
                elif( item.IdMarca == '05'):
                    InyecMarca05 = True
                elif( item.IdMarca == '06'):
                    InyecMarca06 = True
                elif( item.IdMarca == '07'):
                    InyecMarca07 = True
                elif( item.IdMarca == '08'):
                    InyecMarca08 = True
                elif( item.IdMarca == '09'):
                    InyecMarca09 = True
                elif( item.IdMarca == '10'):
                    InyecMarca10 = True
                elif( item.IdMarca == 'Otr'):
                    InyecMarcaOtra = True
            elif ( item.IdMaquina == '04'):
                if  ( item.IdMarca == '01'):
                    LaserMarca01 = True
                elif( item.IdMarca == '02'):
                    LaserMarca02 = True
                elif( item.IdMarca == '03'):
                    LaserMarca03 = True
                elif( item.IdMarca == '04'):
                    LaserMarca04 = True
                elif( item.IdMarca == '05'):
                    LaserMarca05 = True
                elif( item.IdMarca == '06'):
                    LaserMarca06 = True
                elif( item.IdMarca == '07'):
                    LaserMarca07 = True
                elif( item.IdMarca == '08'):
                    LaserMarca08 = True
                elif( item.IdMarca == '09'):
                    LaserMarca09 = True
                elif( item.IdMarca == '10'):
                    LaserMarca10 = True
                elif( item.IdMarca == 'Otr'):
                    LaserMarcaOtra = True
            elif ( item.IdMaquina == '05'):
                if  ( item.IdMarca == '01'):
                    PrensaMarca01 = True
                elif( item.IdMarca == '02'):
                    PrensaMarca02 = True
                elif( item.IdMarca == '03'):
                    PrensaMarca03 = True
                elif( item.IdMarca == '04'):
                    PrensaMarca04 = True
                elif( item.IdMarca == '05'):
                    PrensaMarca05 = True
                elif( item.IdMarca == '06'):
                    PrensaMarca06 = True
                elif( item.IdMarca == '07'):
                    PrensaMarca07 = True
                elif( item.IdMarca == '08'):
                    PrensaMarca08 = True
                elif( item.IdMarca == '09'):
                    PrensaMarca09 = True
                elif( item.IdMarca == '10'):
                    PrensaMarca10 = True
                elif( item.IdMarca == 'Otr'):
                    PrensaMarcaOtra = True
            elif ( item.IdMaquina == '06'):
                if  ( item.IdMarca == '01'):
                    DobladMarca01 = True
                elif( item.IdMarca == '02'):
                    DobladMarca02 = True
                elif( item.IdMarca == '03'):
                    DobladMarca03 = True
                elif( item.IdMarca == '04'):
                    DobladMarca04 = True
                elif( item.IdMarca == '05'):
                    DobladMarca05 = True
                elif( item.IdMarca == '06'):
                    DobladMarca06 = True
                elif( item.IdMarca == '07'):
                    DobladMarca07 = True
                elif( item.IdMarca == '08'):
                    DobladMarca08 = True
                elif( item.IdMarca == '09'):
                    DobladMarca09 = True
                elif( item.IdMarca == '10'):
                    DobladMarca10 = True
                elif( item.IdMarca == 'Otr'):
                    DobladMarcaOtra = True

    datos = {
        "MarcaArrVir01": MarcaArrVir01,
        "MarcaArrVir02": MarcaArrVir02,
        "MarcaArrVir03": MarcaArrVir03,
        "MarcaArrVir04": MarcaArrVir04,
        "MarcaArrVir05": MarcaArrVir05,
        "MarcaArrVir06": MarcaArrVir06,
        "MarcaArrVir07": MarcaArrVir07,
        "MarcaArrVir08": MarcaArrVir08,
        "MarcaArrVir09": MarcaArrVir09,
        "MarcaArrVir10": MarcaArrVir10,
        "MarcaArrVirOtra": MarcaArrVirOtra,
        "ArrVirMarca01": ArrVirMarca01,
        "ArrVirMarca02": ArrVirMarca02,
        "ArrVirMarca03": ArrVirMarca03,
        "ArrVirMarca04": ArrVirMarca04,
        "ArrVirMarca05": ArrVirMarca05,
        "ArrVirMarca06": ArrVirMarca06,
        "ArrVirMarca07": ArrVirMarca07,
        "ArrVirMarca08": ArrVirMarca08,
        "ArrVirMarca09": ArrVirMarca09,
        "ArrVirMarca10": ArrVirMarca10,
        "ArrVirMarcaOtra": ArrVirMarcaOtra,
        "MarcaElectro01": MarcaElectro01,
        "MarcaElectro02": MarcaElectro02,
        "MarcaElectro03": MarcaElectro03,
        "MarcaElectro04": MarcaElectro04,
        "MarcaElectro05": MarcaElectro05,
        "MarcaElectro06": MarcaElectro06,
        "MarcaElectro07": MarcaElectro07,
        "MarcaElectro08": MarcaElectro08,
        "MarcaElectro09": MarcaElectro09,
        "MarcaElectro10": MarcaElectro10,
        "MarcaElectroOtra": MarcaElectroOtra,
        "ElectroMarca01": ElectroMarca01,
        "ElectroMarca02": ElectroMarca02,
        "ElectroMarca03": ElectroMarca03,
        "ElectroMarca04": ElectroMarca04,
        "ElectroMarca05": ElectroMarca05,
        "ElectroMarca06": ElectroMarca06,
        "ElectroMarca07": ElectroMarca07,
        "ElectroMarca08": ElectroMarca08,
        "ElectroMarca09": ElectroMarca09,
        "ElectroMarca10": ElectroMarca10,
        "ElectroMarcaOtra": ElectroMarcaOtra,
        "MarcaInyec01": MarcaInyec01,
        "MarcaInyec02": MarcaInyec02,
        "MarcaInyec03": MarcaInyec03,
        "MarcaInyec04": MarcaInyec04,
        "MarcaInyec05": MarcaInyec05,
        "MarcaInyec06": MarcaInyec06,
        "MarcaInyec07": MarcaInyec07,
        "MarcaInyec08": MarcaInyec08,
        "MarcaInyec09": MarcaInyec09,
        "MarcaInyec10": MarcaInyec10,
        "MarcaInyecOtra": MarcaInyecOtra,
        "InyecMarca01": InyecMarca01,
        "InyecMarca02": InyecMarca02,
        "InyecMarca03": InyecMarca03,
        "InyecMarca04": InyecMarca04,
        "InyecMarca05": InyecMarca05,
        "InyecMarca06": InyecMarca06,
        "InyecMarca07": InyecMarca07,
        "InyecMarca08": InyecMarca08,
        "InyecMarca09": InyecMarca09,
        "InyecMarca10": InyecMarca10,
        "InyecMarcaOtra": InyecMarcaOtra,
        "MarcaLaser01": MarcaLaser01,
        "MarcaLaser02": MarcaLaser02,
        "MarcaLaser03": MarcaLaser03,
        "MarcaLaser04": MarcaLaser04,
        "MarcaLaser05": MarcaLaser05,
        "MarcaLaser06": MarcaLaser06,
        "MarcaLaser07": MarcaLaser07,
        "MarcaLaser08": MarcaLaser08,
        "MarcaLaser09": MarcaLaser09,
        "MarcaLaser10": MarcaLaser10,
        "MarcaLaserOtra": MarcaLaserOtra,
        "LaserMarca01": LaserMarca01,
        "LaserMarca02": LaserMarca02,
        "LaserMarca03": LaserMarca03,
        "LaserMarca04": LaserMarca04,
        "LaserMarca05": LaserMarca05,
        "LaserMarca06": LaserMarca06,
        "LaserMarca07": LaserMarca07,
        "LaserMarca08": LaserMarca08,
        "LaserMarca09": LaserMarca09,
        "LaserMarca10": LaserMarca10,
        "LaserMarcaOtra": LaserMarcaOtra,
        "MarcaPrensa01": MarcaPrensa01,
        "MarcaPrensa02": MarcaPrensa02,
        "MarcaPrensa03": MarcaPrensa03,
        "MarcaPrensa04": MarcaPrensa04,
        "MarcaPrensa05": MarcaPrensa05,
        "MarcaPrensa06": MarcaPrensa06,
        "MarcaPrensa07": MarcaPrensa07,
        "MarcaPrensa08": MarcaPrensa08,
        "MarcaPrensa09": MarcaPrensa09,
        "MarcaPrensa10": MarcaPrensa10,
        "MarcaPrensaOtra": MarcaPrensaOtra,
        "PrensaMarca01": PrensaMarca01,
        "PrensaMarca02": PrensaMarca02,
        "PrensaMarca03": PrensaMarca03,
        "PrensaMarca04": PrensaMarca04,
        "PrensaMarca05": PrensaMarca05,
        "PrensaMarca06": PrensaMarca06,
        "PrensaMarca07": PrensaMarca07,
        "PrensaMarca08": PrensaMarca08,
        "PrensaMarca09": PrensaMarca09,
        "PrensaMarca10": PrensaMarca10,
        "PrensaMarcaOtra": PrensaMarcaOtra,
        "MarcaDoblad01": MarcaDoblad01,
        "MarcaDoblad02": MarcaDoblad02,
        "MarcaDoblad03": MarcaDoblad03,
        "MarcaDoblad04": MarcaDoblad04,
        "MarcaDoblad05": MarcaDoblad05,
        "MarcaDoblad06": MarcaDoblad06,
        "MarcaDoblad07": MarcaDoblad07,
        "MarcaDoblad08": MarcaDoblad08,
        "MarcaDoblad09": MarcaDoblad09,
        "MarcaDoblad10": MarcaDoblad10,
        "MarcaDobladOtra": MarcaDobladOtra,
        "DobladMarca01": DobladMarca01,
        "DobladMarca02": DobladMarca02,
        "DobladMarca03": DobladMarca03,
        "DobladMarca04": DobladMarca04,
        "DobladMarca05": DobladMarca05,
        "DobladMarca06": DobladMarca06,
        "DobladMarca07": DobladMarca07,
        "DobladMarca08": DobladMarca08,
        "DobladMarca09": DobladMarca09,
        "DobladMarca10": DobladMarca10,
        "DobladMarcaOtra": DobladMarcaOtra,
    }

    return datos

def setDataCliente(cliente):
    fecha = cliente.FechaNacimiento
    
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
            #"SucServicio":cliente.SucServicio,
            #"RegionVts":cliente.RegionVts,
            #"iDNielsen":cliente.iDNielsen,
            "NoTurnosC":cliente.NoTurnosC,
            "Tier":cliente.Tier,
            #"FrecuenciaCompra":cliente.FrecuenciaCompra,
            "NoMaqConvenC":cliente.NoMaqConvenC,
            #"NoMaqCNC_C":cliente.NoMaqCNC_C,
            #"NoMaqHT_C":cliente.NoMaqHT_C,
            #"MatUseCHMER":cliente.MatUseCHMER,
            #"MatUseYIZUMI":cliente.MatUseYIZUMI,
            #"MatUsoFab":cliente.MatUsoFab,
            #"MatViruta":cliente.MatViruta,
            #"MatUsoCNC_Haas":cliente.MatUsoCNC_Haas,
            #"ActPriFAB":cliente.ActPriFAB,
            #"ActPriEDM":cliente.ActPriEDM,
            #"ActPriEquipoCNC":cliente.ActPriEquipoCNC,
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
            #"dMatUseCHMER":get_MatUseCHMER(cliente.MatUseCHMER),
            #"dMatUseYIZUMI":get_MatUseYIZUMI(cliente.MatUseYIZUMI),
            #"dMatUsoFab":get_MatUsoFab(cliente.MatUsoFab),
            #"dMatViruta":get_MatViruta(cliente.MatViruta),
            #"dMatUsoCNC_Haas":get_MatUsoCNC_Haas(cliente.MatUsoCNC_Haas),
            #"dRegionVts":get_RegionVts(cliente.RegionVts),
            #"dActPriFAB":get_ActPriFAB(cliente.ActPriFAB),
            #"dActPriEDM":get_ActPriEDM(cliente.ActPriEDM),
            #"dActPriEquipoCNC":get_ActPriEquipoCNC(cliente.ActPriEquipoCNC),
            "dDivHaas":get_DivHaas(cliente.DivHaas),
            "dDivPM":get_DivPM(cliente.DivPM),
            "dDivCNC":get_DivCNC(cliente.DivCNC),
            "dDivHTools":get_DivHTools(cliente.DivHTools),
            "dDivNextec":get_DivNextec(cliente.DivNextec),
            #"DireccioCliente":cliente.DireccioCliente,
            #"TelefonoPrincipal":cliente.TelefonoPrincipal,
            #"RFC":cliente.RFC,
            #"NombreAdicional":cliente.NombreAdicional,
            #"DivisionPM"":cliente.DivisionPM,
            "SitioWeb":cliente.ActPriEquipo,
            "MaqCompArrVir": cliente.MaqCompArrVir,
            "MaqCompElectro": cliente.MaqCompElectro,
            "MaqCompInyec": cliente.MaqCompInyec,
            "MaqCompLaser": cliente.MaqCompLaser,
            "MaqCompPrensa": cliente.MaqCompPrensa,
            "MaqCompDoblad": cliente.MaqCompDoblad,
    }
    return acliente

def editarCliente(request, usrid):
    IdCliente = request.POST['claveExterna']
    NombreCliente = request.POST['NombreCliente']
    #TipoCliente = request.POST['TipoCliente']
    #ClientePotencial = request.POST['ClientePotencial']
    FechaNacimiento = request.POST['FechaNacimiento']
    Sector = request.POST['Sector']
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
    SitioWeb = request.POST['SitioWeb']

    DivHaasMexico = DivHaasEcuador = DivHaasColombia = DivHaasCAM = False
    DivCNCCNC = DivCNCOmnitec = DivHToolsTools = False
    DivNextecFAB = DivNextecEDM = DivPMPM = False
    #DivHToolsSolubles = False
    deleteDivisionCliente(IdCliente)
    if "DivHaasMexico" in request.POST:
        DivHaasMexico = True
        saveDivisionCliente(IdCliente, 1, 109)
    #if "DivHaasEcuador" in request.POST:
    #    DivHaasEcuador = True
    #    saveDivisionCliente(IdCliente, 1, 111)
    #if "DivHaasColombia" in request.POST:
    #    DivHaasColombia = True
    #    saveDivisionCliente(IdCliente, 1, 112)
    #if "DivHaasCAM" in request.POST:
    #    DivHaasCAM = True
    #    saveDivisionCliente(IdCliente, 1, 113)
    if "DivPM" in request.POST:
        DivPMPM = True
        saveDivisionCliente(IdCliente, 2, 116)
    if "DivHToolsTools" in request.POST:
        DivHToolsTools = True
        saveDivisionCliente(IdCliente, 3, 118)
    #if "DivHToolsSolubles" in request.POST:
    #    DivHToolsSolubles = True
    #    saveDivisionCliente(IdCliente, 3, 119)
    if "DivCNCCNC" in request.POST:
        DivCNCCNC = True
        saveDivisionCliente(IdCliente, 4, 121)
    if "DivCNCOmnitec" in request.POST:
        DivCNCOmnitec = True
        saveDivisionCliente(IdCliente, 4, 122)
    if "DivNextecFAB" in request.POST:
        DivNextecFAB = True
        saveDivisionCliente(IdCliente, 5, 123)
    if "DivNextecEDM" in request.POST:
        DivNextecEDM = True
        saveDivisionCliente(IdCliente, 5, 124)
    
    DivHaas   = getVal_DivHaas(DivHaasMexico, DivHaasEcuador, DivHaasColombia, DivHaasCAM)
    DivPM     = getVal_DivPM(DivPMPM)
    DivCNC    = getVal_DivCNC(DivCNCCNC, DivCNCOmnitec)
    DivHTools = getVal_DivHTools(DivHToolsTools, "")
    DivNextec = getVal_DivNextec(DivNextecFAB, DivNextecEDM)
    
    ArrVirMat01 = ArrVirMat02 = ArrVirMat03 = ArrVirMat04 = ArrVirMat05 = ArrVirMat06 = False
    ElectroMat01 = ElectroMat02 = ElectroMat03 = ElectroMat04 = ElectroMat05 = ElectroMat06 = ElectroMat07 = False
    InyecMat01 = InyecMat02 = InyecMat03 = InyecMat04 = InyecMat05 = InyecMat06 = InyecMat07 = False
    FABMat01 = FABMat02 = FABMat03 = FABMat04 = FABMat05 = False
    deleteMaterialCliente(IdCliente)
    if "ArrVirMat01" in request.POST:
        ArrVirMat01 = True
        saveMaterialCliente(IdCliente, '01', '163')
    if "ArrVirMat02" in request.POST:
        ArrVirMat02 = True
        saveMaterialCliente(IdCliente, '01', '164')
    if "ArrVirMat03" in request.POST:
        ArrVirMat03 = True
        saveMaterialCliente(IdCliente, '01', '165')
    if "ArrVirMat04" in request.POST:
        ArrVirMat04 = True
        saveMaterialCliente(IdCliente, '01', '166')
    if "ArrVirMat05" in request.POST:
        ArrVirMat05 = True
        saveMaterialCliente(IdCliente, '01', '167')
    if "ArrVirMat06" in request.POST:
        ArrVirMat06 = True
        saveMaterialCliente(IdCliente, '01', '168')
    if "ElectroMat01" in request.POST:
        ElectroMat01 = True
        saveMaterialCliente(IdCliente, '02', '170')
    if "ElectroMat02" in request.POST:
        ElectroMat02 = True
        saveMaterialCliente(IdCliente, '02', '171')
    if "ElectroMat03" in request.POST:
        ElectroMat03 = True
        saveMaterialCliente(IdCliente, '02', '172')
    if "ElectroMat04" in request.POST:
        ElectroMat04 = True
        saveMaterialCliente(IdCliente, '02', '173')
    if "ElectroMat05" in request.POST:
        ElectroMat05 = True
        saveMaterialCliente(IdCliente, '02', '174')
    if "ElectroMat06" in request.POST:
        ElectroMat06 = True
        saveMaterialCliente(IdCliente, '02', '175')
    if "ElectroMat07" in request.POST:
        ElectroMat07 = True
        saveMaterialCliente(IdCliente, '02', '176')
    if "InyecMat01" in request.POST:
        InyecMat01 = True
        saveMaterialCliente(IdCliente, '03', '179')
    if "InyecMat02" in request.POST:
        InyecMat02 = True
        saveMaterialCliente(IdCliente, '03', '180')
    if "InyecMat03" in request.POST:
        InyecMat03 = True
        saveMaterialCliente(IdCliente, '03', '181')
    if "InyecMat04" in request.POST:
        InyecMat04 = True
        saveMaterialCliente(IdCliente, '03', '182')
    if "InyecMat05" in request.POST:
        InyecMat05 = True
        saveMaterialCliente(IdCliente, '03', '183')
    if "InyecMat06" in request.POST:
        InyecMat06 = True
        saveMaterialCliente(IdCliente, '03', '184')
    if "InyecMat07" in request.POST:
        InyecMat07 = True
        saveMaterialCliente(IdCliente, '03', '185')
    if "FABMat01" in request.POST:
        FABMat01 = True
        saveMaterialCliente(IdCliente, '04', '187')
    if "FABMat02" in request.POST:
        FABMat02 = True
        saveMaterialCliente(IdCliente, '04', '188')
    if "FABMat03" in request.POST:
        FABMat03 = True
        saveMaterialCliente(IdCliente, '04', '189')
    if "FABMat04" in request.POST:
        FABMat04 = True
        saveMaterialCliente(IdCliente, '04', '190')
    if "FABMat05" in request.POST:
        FABMat05 = True
        saveMaterialCliente(IdCliente, '04', '191')

    MatViruta = getVal_MatUseArrVir(ArrVirMat01, ArrVirMat02, ArrVirMat03, ArrVirMat04, ArrVirMat05, ArrVirMat06)
    MatUseCHMER = getVal_MatUseElectro(ElectroMat01, ElectroMat02, ElectroMat03, ElectroMat04, ElectroMat05, ElectroMat06, ElectroMat07)
    MatUseYIZUMI = getVal_MatUseInyec(InyecMat01, InyecMat02, InyecMat03, InyecMat04, InyecMat05, InyecMat06, InyecMat07)
    MatUsoFab = getVal_MatUseFAB(FABMat01, FABMat02, FABMat03, FABMat04, FABMat05)
    
    MaqCompArrVir = request.POST['MaqCompArrVir']
    MaqCompElectro = request.POST['MaqCompElectro']
    MaqCompInyec = request.POST['MaqCompInyec']
    MaqCompLaser = request.POST['MaqCompLaser']
    MaqCompPrensa = request.POST['MaqCompPrensa']
    MaqCompDoblad = request.POST['MaqCompDoblad']

    deleteMaquinaCliente(IdCliente)
    
    MarcaArrVirOtra = request.POST['MarcaArrVirOtra']
    MarcaElectroOtra = request.POST['MarcaElectroOtra']
    MarcaInyecOtra = request.POST['MarcaInyecOtra']
    MarcaLaserOtra = request.POST['MarcaLaserOtra']
    MarcaPrensaOtra = request.POST['MarcaPrensaOtra']
    MarcaDobladOtra = request.POST['MarcaDobladOtra']

    ArrVirMarca01 = ArrVirMarca02 = ArrVirMarca03 = ArrVirMarca04 = ArrVirMarca05 = False
    ArrVirMarca06 = ArrVirMarca07 = ArrVirMarca08 = ArrVirMarca09 = ArrVirMarca10 = ArrVirMarcaOtra = False
    if "ArrVirMarca01" in request.POST:
        ArrVirMarca01 = True
        saveMaquinaCliente(IdCliente, '01', '01', 'Dn Solutions')
    if "ArrVirMarca02" in request.POST:
        ArrVirMarca02 = True
        saveMaquinaCliente(IdCliente, '01', '02', 'Okuma')
    if "ArrVirMarca03" in request.POST:
        ArrVirMarca03 = True
        saveMaquinaCliente(IdCliente, '01', '03', 'Dmg Mori')
    if "ArrVirMarca04" in request.POST:
        ArrVirMarca04 = True
        saveMaquinaCliente(IdCliente, '01', '04', 'Mazak')
    if "ArrVirMarca05" in request.POST:
        ArrVirMarca05 = True
        saveMaquinaCliente(IdCliente, '01', '05', 'Hision')
    if "ArrVirMarca06" in request.POST:
        ArrVirMarca06 = True
        saveMaquinaCliente(IdCliente, '01', '06', 'Hyundai')
    if "ArrVirMarca07" in request.POST:
        ArrVirMarca07 = True
        saveMaquinaCliente(IdCliente, '01', '07', 'Baoji')
    if "ArrVirMarca08" in request.POST:
        ArrVirMarca08 = True
        saveMaquinaCliente(IdCliente, '01', '08', 'Makino')
    if "ArrVirMarca09" in request.POST:
        ArrVirMarca09 = True
        saveMaquinaCliente(IdCliente, '01', '09', 'Romi')
    if "ArrVirMarca10" in request.POST:
        ArrVirMarca10 = True
        saveMaquinaCliente(IdCliente, '01', '10', 'Chiron')
    if "ArrVirMarcaOtra" in request.POST:
        ArrVirMarcaOtra = True
        saveMaquinaCliente(IdCliente, '01', 'Otr', MarcaArrVirOtra)
    
    ElectroMarca01 = ElectroMarca02 = ElectroMarca03 = ElectroMarca04 = ElectroMarca05 = False
    ElectroMarca06 = ElectroMarca07 = ElectroMarca08 = ElectroMarca09 = ElectroMarca10 = ElectroMarcaOtra = False
    if "ElectroMarca01" in request.POST:
        ElectroMarca01 = True
        saveMaquinaCliente(IdCliente, '02', '01', 'Sodick')
    if "ElectroMarca02" in request.POST:
        ElectroMarca02 = True
        saveMaquinaCliente(IdCliente, '02', '02', 'Mitsubishi')
    if "ElectroMarca03" in request.POST:
        ElectroMarca03 = True
        saveMaquinaCliente(IdCliente, '02', '03', 'Shem')
    if "ElectroMarca04" in request.POST:
        ElectroMarca04 = True
        saveMaquinaCliente(IdCliente, '02', '04', 'Accutex')
    if "ElectroMarca05" in request.POST:
        ElectroMarca05 = True
        saveMaquinaCliente(IdCliente, '02', '05', 'Makino')
    if "ElectroMarca06" in request.POST:
        ElectroMarca06 = True
        saveMaquinaCliente(IdCliente, '02', '06', 'Ipretech')
    if "ElectroMarca07" in request.POST:
        ElectroMarca07 = True
        saveMaquinaCliente(IdCliente, '02', '07', 'Mc-Lane')
    if "ElectroMarca08" in request.POST:
        ElectroMarca08 = True
        saveMaquinaCliente(IdCliente, '02', '08', 'Excetek')
    if "ElectroMarca09" in request.POST:
        ElectroMarca09 = True
        saveMaquinaCliente(IdCliente, '02', '09', 'Maincasa')
    if "ElectroMarca10" in request.POST:
        ElectroMarca10 = True
        saveMaquinaCliente(IdCliente, '02', '10', 'Protecnic')
    if "ElectroMarcaOtra" in request.POST:
        ElectroMarcaOtra = True
        saveMaquinaCliente(IdCliente, '02', 'Otr', MarcaElectroOtra)
    
    InyecMarca01 = InyecMarca02 = InyecMarca03 = InyecMarca04 = InyecMarca05 = False
    InyecMarca06 = InyecMarca07 = InyecMarca08 = InyecMarca09 = InyecMarca10 = InyecMarcaOtra = False
    if "InyecMarca01" in request.POST:
        InyecMarca01 = True
        saveMaquinaCliente(IdCliente, '03', '01', 'Haitian')
    if "InyecMarca02" in request.POST:
        InyecMarca02 = True
        saveMaquinaCliente(IdCliente, '03', '02', 'Engel')
    if "InyecMarca03" in request.POST:
        InyecMarca03 = True
        saveMaquinaCliente(IdCliente, '03', '03', 'Sumitomo')
    if "InyecMarca04" in request.POST:
        InyecMarca04 = True
        saveMaquinaCliente(IdCliente, '03', '04', 'Krauss Maffei')
    if "InyecMarca05" in request.POST:
        InyecMarca05 = True
        saveMaquinaCliente(IdCliente, '03', '05', 'Nissei')
    if "InyecMarca06" in request.POST:
        InyecMarca06 = True
        saveMaquinaCliente(IdCliente, '03', '06', 'Borche')
    if "InyecMarca07" in request.POST:
        InyecMarca07 = True
        saveMaquinaCliente(IdCliente, '03', '07', 'Arburg')
    if "InyecMarca08" in request.POST:
        InyecMarca08 = True
        saveMaquinaCliente(IdCliente, '03', '08', 'CLF')
    if "InyecMarca09" in request.POST:
        InyecMarca09 = True
        saveMaquinaCliente(IdCliente, '03', '09', 'Tai-Mex')
    if "InyecMarca10" in request.POST:
        InyecMarca10 = True
        saveMaquinaCliente(IdCliente, '03', '10', 'Bole')
    if "InyecMarcaOtra" in request.POST:
        InyecMarcaOtra = True
        saveMaquinaCliente(IdCliente, '03', 'Otr', MarcaInyecOtra)
    
    LaserMarca01 = LaserMarca02 = LaserMarca03 = LaserMarca04 = LaserMarca05 = False
    LaserMarca06 = LaserMarca07 = LaserMarca08 = LaserMarca09 = LaserMarca10 = LaserMarcaOtra = False
    if "LaserMarca01" in request.POST:
        LaserMarca01 = True
        saveMaquinaCliente(IdCliente, '04', '01', 'Bodor')
    if "LaserMarca02" in request.POST:
        LaserMarca02 = True
        saveMaquinaCliente(IdCliente, '04', '02', 'Gweike')
    if "LaserMarca03" in request.POST:
        LaserMarca03 = True
        saveMaquinaCliente(IdCliente, '04', '03', 'Trumpf')
    if "LaserMarca04" in request.POST:
        LaserMarca04 = True
        saveMaquinaCliente(IdCliente, '04', '04', 'Bimex')
    if "LaserMarca05" in request.POST:
        LaserMarca05 = True
        saveMaquinaCliente(IdCliente, '04', '05', 'Durma')
    if "LaserMarca06" in request.POST:
        LaserMarca06 = True
        saveMaquinaCliente(IdCliente, '04', '06', 'Aida')
    if "LaserMarca07" in request.POST:
        LaserMarca07 = True
        saveMaquinaCliente(IdCliente, '04', '07', 'Amada')
    if "LaserMarca08" in request.POST:
        LaserMarca08 = True
        saveMaquinaCliente(IdCliente, '04', '08', 'JFY')
    if "LaserMarca09" in request.POST:
        LaserMarca09 = True
        saveMaquinaCliente(IdCliente, '04', '09', 'Bystronic')
    if "LaserMarca10" in request.POST:
        LaserMarca10 = True
        saveMaquinaCliente(IdCliente, '04', '10', 'BLM')
    if "LaserMarcaOtra" in request.POST:
        LaserMarcaOtra = True
        saveMaquinaCliente(IdCliente, '04', 'Otr', MarcaLaserOtra)
    
    PrensaMarca01 = PrensaMarca02 = PrensaMarca03 = PrensaMarca04 = PrensaMarca05 = False
    PrensaMarca06 = PrensaMarca07 = PrensaMarca08 = PrensaMarca09 = PrensaMarca10 = PrensaMarcaOtra = False
    if "PrensaMarca01" in request.POST:
        PrensaMarca01 = True
        saveMaquinaCliente(IdCliente, '05', '01', 'Fagor')
    if "PrensaMarca02" in request.POST:
        PrensaMarca02 = True
        saveMaquinaCliente(IdCliente, '05', '02', 'Aida')
    if "PrensaMarca03" in request.POST:
        PrensaMarca03 = True
        saveMaquinaCliente(IdCliente, '05', '03', 'Simpac')
    if "PrensaMarca04" in request.POST:
        PrensaMarca04 = True
        saveMaquinaCliente(IdCliente, '05', '04', 'Shem')
    if "PrensaMarca05" in request.POST:
        PrensaMarca05 = True
        saveMaquinaCliente(IdCliente, '05', '05', 'Amada')
    if "PrensaMarca06" in request.POST:
        PrensaMarca06 = True
        saveMaquinaCliente(IdCliente, '05', '06', 'Komatsu')
    if "PrensaMarca07" in request.POST:
        PrensaMarca07 = True
        saveMaquinaCliente(IdCliente, '05', '07', 'Schuler')
    if "PrensaMarca08" in request.POST:
        PrensaMarca08 = True
        saveMaquinaCliente(IdCliente, '05', '08', 'Marubeni')
    if "PrensaMarca09" in request.POST:
        PrensaMarca09 = True
        saveMaquinaCliente(IdCliente, '05', '09', 'Mitsubishi')
    if "PrensaMarca10" in request.POST:
        PrensaMarca10 = True
        saveMaquinaCliente(IdCliente, '05', '10', 'Seyi')
    if "PrensaMarcaOtra" in request.POST:
        PrensaMarcaOtra = True
        saveMaquinaCliente(IdCliente, '05', 'Otr', MarcaPrensaOtra)
    
    DobladMarca01 = DobladMarca02 = DobladMarca03 = DobladMarca04 = DobladMarca05 = False
    DobladMarca06 = DobladMarca07 = DobladMarca08 = DobladMarca09 = DobladMarca10 = DobladMarcaOtra = False
    if "DobladMarca01" in request.POST:
        DobladMarca01 = True
        saveMaquinaCliente(IdCliente, '06', '01', 'Durma')
    if "DobladMarca02" in request.POST:
        DobladMarca02 = True
        saveMaquinaCliente(IdCliente, '06', '02', 'Amada')
    if "DobladMarca03" in request.POST:
        DobladMarca03 = True
        saveMaquinaCliente(IdCliente, '06', '03', 'Shem')
    if "DobladMarca04" in request.POST:
        DobladMarca04 = True
        saveMaquinaCliente(IdCliente, '06', '04', 'Bystronic')
    if "DobladMarca05" in request.POST:
        DobladMarca05 = True
        saveMaquinaCliente(IdCliente, '06', '05', 'Yawei')
    if "DobladMarca06" in request.POST:
        DobladMarca06 = True
        saveMaquinaCliente(IdCliente, '06', '06', 'Amob')
    if "DobladMarca07" in request.POST:
        DobladMarca07 = True
        saveMaquinaCliente(IdCliente, '06', '07', 'Trumpf')
    if "DobladMarca08" in request.POST:
        DobladMarca08 = True
        saveMaquinaCliente(IdCliente, '06', '08', 'BLM')
    if "DobladMarca09" in request.POST:
        DobladMarca09 = True
        saveMaquinaCliente(IdCliente, '06', '09', 'Nargesa')
    if "DobladMarca10" in request.POST:
        DobladMarca10 = True
        saveMaquinaCliente(IdCliente, '06', '10', 'MVD')
    if "DobladMarcaOtra" in request.POST:
        DobladMarcaOtra = True
        saveMaquinaCliente(IdCliente, '06', 'Otr', MarcaDobladOtra)
    
    #ActPriFAB = ActPriEDM = ActPriEquipoCNC = ""
    #if "ActPriFAB" in request.POST:
    #    ActPriFAB = request.POST['ActPriFAB']
    #if "ActPriEDM" in request.POST:
    #    ActPriEDM = request.POST['ActPriEDM']
    #if "ActPriEquipoCNC" in request.POST:
    #    ActPriEquipoCNC = request.POST['ActPriEquipoCNC']
        
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
    cliente.ActPriEquipo = SitioWeb
    cliente.DivHaas = DivHaas
    cliente.DivPM = DivPM
    cliente.DivCNC = DivCNC
    cliente.DivHTools = DivHTools
    cliente.DivNextec = DivNextec
    cliente.MaqCompArrVir = MaqCompArrVir
    cliente.MaqCompElectro = MaqCompElectro
    cliente.MaqCompInyec = MaqCompInyec
    cliente.MaqCompLaser = MaqCompLaser
    cliente.MaqCompPrensa = MaqCompPrensa
    cliente.MaqCompDoblad = MaqCompDoblad
    cliente.save()

    divisiones = {
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
    materiales = {
        "ArrVirMat01": ArrVirMat01,
        "ArrVirMat02": ArrVirMat02,
        "ArrVirMat03": ArrVirMat03,
        "ArrVirMat04": ArrVirMat04,
        "ArrVirMat05": ArrVirMat05,
        "ArrVirMat06": ArrVirMat06,
        "ElectroMat01": ElectroMat01,
        "ElectroMat02": ElectroMat02,
        "ElectroMat03": ElectroMat03,
        "ElectroMat04": ElectroMat04,
        "ElectroMat05": ElectroMat05,
        "ElectroMat06": ElectroMat06,
        "ElectroMat07": ElectroMat07,
        "InyecMat01": InyecMat01,
        "InyecMat02": InyecMat02,
        "InyecMat03": InyecMat03,
        "InyecMat04": InyecMat04,
        "InyecMat05": InyecMat05,
        "InyecMat06": InyecMat06,
        "InyecMat07": InyecMat07,
        "FABMat01": FABMat01,
        "FABMat02": FABMat02,
        "FABMat03": FABMat03,
        "FABMat04": FABMat04,
        "FABMat05": FABMat05,
    }
    marcasMaq = {
        "ArrVirMarca01": ArrVirMarca01,
        "ArrVirMarca02": ArrVirMarca02,
        "ArrVirMarca03": ArrVirMarca03,
        "ArrVirMarca04": ArrVirMarca04,
        "ArrVirMarca05": ArrVirMarca05,
        "ArrVirMarca06": ArrVirMarca06,
        "ArrVirMarca07": ArrVirMarca07,
        "ArrVirMarca08": ArrVirMarca08,
        "ArrVirMarca09": ArrVirMarca09,
        "ArrVirMarca10": ArrVirMarca10,
        "ArrVirMarcaOtra": ArrVirMarcaOtra,
        "ElectroMarca01": ElectroMarca01,
        "ElectroMarca02": ElectroMarca02,
        "ElectroMarca03": ElectroMarca03,
        "ElectroMarca04": ElectroMarca04,
        "ElectroMarca05": ElectroMarca05,
        "ElectroMarca06": ElectroMarca06,
        "ElectroMarca07": ElectroMarca07,
        "ElectroMarca08": ElectroMarca08,
        "ElectroMarca09": ElectroMarca09,
        "ElectroMarca10": ElectroMarca10,
        "ElectroMarcaOtra": ElectroMarcaOtra,
        "InyecMarca01": InyecMarca01,
        "InyecMarca02": InyecMarca02,
        "InyecMarca03": InyecMarca03,
        "InyecMarca04": InyecMarca04,
        "InyecMarca05": InyecMarca05,
        "InyecMarca06": InyecMarca06,
        "InyecMarca07": InyecMarca07,
        "InyecMarca08": InyecMarca08,
        "InyecMarca09": InyecMarca09,
        "InyecMarca10": InyecMarca10,
        "InyecMarcaOtra": InyecMarcaOtra,
        "LaserMarca01": LaserMarca01,
        "LaserMarca02": LaserMarca02,
        "LaserMarca03": LaserMarca03,
        "LaserMarca04": LaserMarca04,
        "LaserMarca05": LaserMarca05,
        "LaserMarca06": LaserMarca06,
        "LaserMarca07": LaserMarca07,
        "LaserMarca08": LaserMarca08,
        "LaserMarca09": LaserMarca09,
        "LaserMarca10": LaserMarca10,
        "LaserMarcaOtra": LaserMarcaOtra,
        "PrensaMarca01": PrensaMarca01,
        "PrensaMarca02": PrensaMarca02,
        "PrensaMarca03": PrensaMarca03,
        "PrensaMarca04": PrensaMarca04,
        "PrensaMarca05": PrensaMarca05,
        "PrensaMarca06": PrensaMarca06,
        "PrensaMarca07": PrensaMarca07,
        "PrensaMarca08": PrensaMarca08,
        "PrensaMarca09": PrensaMarca09,
        "PrensaMarca10": PrensaMarca10,
        "PrensaMarcaOtra": PrensaMarcaOtra,
        "DobladMarca01": DobladMarca01,
        "DobladMarca02": DobladMarca02,
        "DobladMarca03": DobladMarca03,
        "DobladMarca04": DobladMarca04,
        "DobladMarca05": DobladMarca05,
        "DobladMarca06": DobladMarca06,
        "DobladMarca07": DobladMarca07,
        "DobladMarca08": DobladMarca08,
        "DobladMarca09": DobladMarca09,
        "DobladMarca10": DobladMarca10,
        "DobladMarcaOtra": DobladMarcaOtra,
    }

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
        "SitioWeb": SitioWeb,
        "divisiones": divisiones,
        "materiales": materiales,
        "marcasMaq": marcasMaq,
    }

    addLog(usrid, "Update", "Clientes", IdCliente, data)
    messages.success(request, "Los datos del cliente fueron actualizados con éxito")
    return redirect('/edicionCliente/'+IdCliente+'/'+usrid)
    #return redirect('/home/'+usrid)

def deleteDivisionCliente(codigo):
    if divisionCliente.objects.filter(IdContacto=codigo).exists():
        registro = divisionCliente.objects.all().filter(IdContacto=codigo)
        registro.delete()
    return

def saveDivisionCliente(codigo, IdDivision, IdSubdivision):
    if divisionCliente.objects.filter(IdContacto=codigo, IdDivision=IdDivision, IdSubdivision=IdSubdivision).exists():
        return
    else:
        registro = divisionCliente.objects.create (
            IdContacto = codigo,
            IdDivision = IdDivision,
            IdSubdivision = IdSubdivision
        )
        return

def deleteMaterialCliente(codigo):
    if MaterialCliente.objects.filter(IdCliente=codigo).exists():
        registro = MaterialCliente.objects.all().filter(IdCliente=codigo)
        registro.delete()
    return

def saveMaterialCliente(codigo, IdMaterial, IdTipo):
    if MaterialCliente.objects.filter(IdCliente=codigo, IdMaterial=IdMaterial, IdTipo=IdTipo).exists():
        return
    else:
        registro = MaterialCliente.objects.create (
            IdCliente = codigo,
            IdMaterial = IdMaterial,
            IdTipo = IdTipo
        )
        return

def deleteMaquinaCliente(codigo):
    if MaquinasCliente.objects.filter(IdCliente=codigo).exists():
        registro = MaquinasCliente.objects.all().filter(IdCliente=codigo)
        registro.delete()
    return

def saveMaquinaCliente(codigo, IdMaquina, IdMarca, Marca):
    if MaquinasCliente.objects.filter(IdCliente=codigo, IdMaquina=IdMaquina, IdMarca=IdMarca).exists():
        return
    else:
        registro = MaquinasCliente.objects.create (
            IdCliente = codigo,
            IdMaquina = IdMaquina,
            IdMarca = IdMarca,
            Marca = Marca
        )
        return

def gestionContactos(request, codigo, usrid):
    session = getSession(usrid)
    cliente = Clientes.objects.get(IdCliente=codigo)
    if Contactos.objects.filter(IdCliente=codigo).exists():
    # Si el cliente tiene contactos envía el listado de contactos del cliente
        contactosListados = Contactos.objects.all().filter(IdCliente=codigo)
        contactosListadosOK = []
        for item in contactosListados.iterator():
            item.Funcion = get_Funcion(item.Funcion)
            contactosListadosOK.append(item)

        return render(request,"gestionContactos.html",{"contactos":contactosListadosOK, "cliente":cliente, "session":session})
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
    division = getDivisiones(codigo)
    
    return render(request, "edicionContactos.html",{"vista":"Contacto", "Gestion":Gestion, "idRegistro":codigo, "contacto":contacto, "cliente":cliente, "session":session, "logData":getLogData('Contactos', codigo), "iniPais":iniPais, "iniRegion":iniRegion, "iniCodPos":iniCodPos, "iniDistrito":iniDistrito, "dataInt":dataInt, "iniCheckbox":iniCheckbox, "descrip": descrip, "division":division })

#Obtiene la descripción de campos por su Id para mostrar en el formulario
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

#Obtiene las divisiones registradas del Contacto
def getDivisiones(codigo):
    HaasMexico = HaasColombia = HaasCAM = HaasEcuador = False
    NextecMachinery = AGPlastic = HitecCNC = HitecTools = False
    if DivisionContacto.objects.filter(IdContacto=codigo).exists():
        divisiones = DivisionContacto.objects.all().filter(IdContacto=codigo)
        for item in divisiones.iterator():
            if (item.Division == 'Haas México'):
                HaasMexico = True
            elif (item.Division == 'Haas CAM') :
                HaasCAM = True
            elif (item.Division == 'Haas Colombia') :
                HaasColombia = True
            elif (item.Division == 'Haas Ecuador') :
                HaasEcuador = True
            elif (item.Division == 'Hitec CNC Maquinaria de México') :
                HitecCNC = True
            elif (item.Division == 'Hitec Tools') :
                HitecTools = True
            elif (item.Division == 'Nexttec Machinery') :
                NextecMachinery = True
            elif (item.Division == 'A&G Plastic Machinery') :
                AGPlastic= True

    divisiones = {
        "HaasMexico": HaasMexico,
        "HaasColombia": HaasColombia,
        "HaasCAM": HaasCAM,
        "HaasEcuador": HaasEcuador,
        "NextecMachinery": NextecMachinery,
        "AGPlastic": AGPlastic,
        "HitecCNC": HitecCNC,
        "HitecTools": HitecTools
    }
    return divisiones

#Actualiza o crea un Contacto
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

    #Actualiza divisiones
    HaasMexico = HaasColombia = HaasCAM = HaasEcuador = False
    NextecMachinery = AGPlastic = HitecCNC = HitecTools = False
    deleteDivisionContacto(IdContacto)

    if "HaasMexico" in request.POST:
        HaasMexico = True
        saveDivisionContacto(IdContacto, 'Haas México')
    if "HaasColombia" in request.POST:
        HaasColombia = True
        saveDivisionContacto(IdContacto, 'Haas Colombia')
    if "HaasCAM" in request.POST:
        HaasCAM = True
        saveDivisionContacto(IdContacto, 'Haas CAM')
    if "HaasEcuador" in request.POST:
        HaasEcuador = True
        saveDivisionContacto(IdContacto, 'Haas Ecuador')
    if "NextecMachinery" in request.POST:
        NextecMachinery = True
        saveDivisionContacto(IdContacto, 'Nexttec Machinery')
    if "AGPlastic" in request.POST:
        AGPlastic = True
        saveDivisionContacto(IdContacto, 'A&G Plastic Machinery')
    if "HitecCNC" in request.POST:
        HitecCNC = True
        saveDivisionContacto(IdContacto, 'Hitec CNC Maquinaria de México')
    if "HitecTools" in request.POST:
        HitecTools = True
        saveDivisionContacto(IdContacto, 'Hitec Tools')
            
    #saveDivisionContacto(IdContacto, 'Haas México', HaasMexico)
    #saveDivisionContacto(IdContacto, 'Haas Colombia', HaasColombia)
    #saveDivisionContacto(IdContacto, 'Haas CAM', HaasCAM)
    #saveDivisionContacto(IdContacto, 'Haas Ecuador', HaasEcuador)
    #saveDivisionContacto(IdContacto, 'Nexttec Machinery', NextecMachinery)
    #saveDivisionContacto(IdContacto, 'A&G Plastic Machinery', AGPlastic)
    #saveDivisionContacto(IdContacto, 'Hitec CNC Maquinaria de México', HitecCNC)
    #saveDivisionContacto(IdContacto, 'Hitec Tools', HitecTools)

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
            "Vip": Vip,
            "HaasMexico": HaasMexico,
            "HaasColombia": HaasColombia,
            "HaasCAM": HaasCAM,
            "HaasEcuador": HaasEcuador,
            "NextecMachinery": NextecMachinery,
            "AGPlastic": AGPlastic,
            "HitecCNC": HitecCNC,
            "HitecTools": HitecTools,
    }

    entidad = "Contactos"
    addLog(usrid, movimiento, entidad, IdContacto, data)
    return redirect('/edicionContacto/'+IdCliente+'/'+IdContacto+'/Gestion/'+usrid)
    #return redirect("../gestionContactos/"+IdCliente+"/"+usrid)

#Elimina las divisiones del Contacto
def deleteDivisionContacto(codigo):
    if DivisionContacto.objects.filter(IdContacto=codigo).exists():
        registro = DivisionContacto.objects.all().filter(IdContacto=codigo)
        registro.delete()
    return

#Registra las divisiones del Contacto
def saveDivisionContacto(codigo, Division):
    if DivisionContacto.objects.filter(IdContacto=codigo, Division=Division).exists():
        return
    else:
        division = DivisionContacto.objects.create (
            IdContacto = codigo,
            Division = Division
        )
        return

#Bloqueo (Inativación) / Desbloqueo (Activación)
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
    contactosListadosOK = []
    for item in contactosListados.iterator():
        item.Funcion = get_Funcion(item.Funcion)
        contactosListadosOK.append(item)
    return render(request,"gestionContactos.html",{"contactos":contactosListadosOK, "cliente":cliente, "session":session})

def eliminarContacto(request,contacto,cliente):
    contacto = Contactos.objects.get(IdContacto=contacto)
    contacto.delete()
    contactosListados = Contactos.objects.all().filter(IdCliente=cliente)
    contactosListadosOK = []
    for item in contactosListados.iterator():
        item.Funcion = get_Funcion(item.Funcion)
        contactosListadosOK.append(item)
    return render(request,"gestionContactos.html",{"contactos":contactosListadosOK})

def gestionDirecciones(request,codigo, usrid):
    session = getSession(usrid) 
    cliente = Clientes.objects.get(IdCliente=codigo)
    if Direcciones.objects.filter(IdCliente=codigo).exists():
        direccionesListados = Direcciones.objects.all().filter(IdCliente=codigo)
        direccionesListadosOK = []
        for item in direccionesListados.iterator():
            IdPais=item.PaisRegion
            item.PaisRegion = getDescripPais(item.PaisRegion)
            item.Estado = getDescripRegion(IdPais,item.Estado)
            direccionesListadosOK.append(item)

    # Si hay direcciones, se envía a gestión de direcciones
        return render(request,"gestionDirecciones.html",{"direcciones":direccionesListadosOK, "cliente":cliente, "session":session})
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
                    if Region.objects.filter(IdCountry=idPais, CodeId=direcciones.CodigoDomFiscal).exists():
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

#Valida que exista el registro de la división del cliente
def validDivision(IdCliente, IdDiv, IdSubDiv):
    if divisionCliente.objects.filter(IdContacto=IdCliente, IdDivision=IdDiv, IdSubdivision=IdSubDiv).exists():
        return True
    else:
        return False   

def validMarca(IdCliente, IdMaquina, IdMarca):
    if MaquinasCliente.objects.filter(IdCliente=IdCliente, IdMaquina=IdMaquina, IdMarca=IdMarca).exists():
        return True
    else:
        return False   
    
def getMarca(IdCliente, IdMaquina, IdMarca):
    descrip = ""
    if MaquinasCliente.objects.filter(IdCliente=IdCliente, IdMaquina=IdMaquina, IdMarca=IdMarca).exists():
        marca = MaquinasCliente.objects.get(IdCliente=IdCliente, IdMaquina=IdMaquina, IdMarca=IdMarca)
        descrip = marca.Marca
    return descrip  

def validOtra(flag, valor) :
    if flag :
        if  valor == '' :
            flag = False
    else :
        if valor != "" :
            flag = True
    return flag

def validMaterial(IdCliente, IdMaterial, IdTipo):
    if MaterialCliente.objects.filter(IdCliente=IdCliente, IdMaterial=IdMaterial, IdTipo=IdTipo).exists():
        return True
    else:
        return False   
    
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

def getDescripPais(codigo):
    descrip = ""
    if Country.objects.filter(CodeId=codigo).exists():
        pais = Country.objects.get(CodeId=codigo)
        descrip = pais.Descrip
    return descrip

def getDescripRegion(IdCountry, codigo):
    descrip = ""
    if Region.objects.filter(IdCountry=IdCountry, CodeId=codigo).exists():
        region = Region.objects.get(IdCountry=IdCountry, CodeId=codigo)
        descrip = region.Descrip
    return descrip

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
    if   (codigo == 'Haas CAM') :                           descrip = 'Haas CAM'
    elif (codigo == 'Haas Colombia') :                      descrip = 'Haas Colombia'
    elif (codigo == 'Haas Ecuador') :                       descrip = 'Haas Ecuador'
    elif (codigo == 'Haas México') :                        descrip = 'Haas México'
    elif (codigo == 'Hitec CNC Maquinaria de México') :     descrip = 'Hitec CNC Maquinaria de México'
    elif (codigo == 'Hitec Tools') :                        descrip = 'Hitec Tools'
    elif (codigo == 'Nexttec Machinery') :                  descrip = 'Nexttec Machinery'
    elif (codigo == 'A&G Plastic Machinery') :              descrip = 'A&G Plastic Machinery'
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


def getVal_MatUseArrVir(ArrVirMat01, ArrVirMat02, ArrVirMat03, ArrVirMat04, ArrVirMat05, ArrVirMat06) :
    codigo = ""
    if   (ArrVirMat01):      codigo = '163'
    elif (ArrVirMat02):      codigo = '164'
    elif (ArrVirMat03):      codigo = '165'
    elif (ArrVirMat04):      codigo = '166'
    elif (ArrVirMat05):      codigo = '167'
    elif (ArrVirMat06):      codigo = '168'
    return (codigo)

def getVal_MatUseElectro(ElectroMat01, ElectroMat02, ElectroMat03, ElectroMat04, ElectroMat05, ElectroMat06, ElectroMat07) :
    codigo = ""
    if   (ElectroMat01): codigo = '170'
    elif (ElectroMat02):      codigo = '171'
    elif (ElectroMat03):      codigo = '172'
    elif (ElectroMat04):      codigo = '173'
    elif (ElectroMat05):      codigo = '174'
    elif (ElectroMat06):      codigo = '175'
    elif (ElectroMat07):      codigo = '176'
    return (codigo)

def getVal_MatUseInyec(InyecMat01, InyecMat02, InyecMat03, InyecMat04, InyecMat05, InyecMat06, InyecMat07) :
    codigo = ""
    if   (InyecMat01): codigo = '179'
    elif (InyecMat02):      codigo = '180'
    elif (InyecMat03):      codigo = '181'
    elif (InyecMat04):      codigo = '182'
    elif (InyecMat05):      codigo = '183'
    elif (InyecMat06):      codigo = '184'
    elif (InyecMat07):      codigo = '185'
    return (codigo)

def getVal_MatUseFAB(FABMat01, FABMat02, FABMat03, FABMat04, FABMat05) :
    codigo = ""
    if   (FABMat01):      codigo = '187'
    elif (FABMat02):      codigo = '188'
    elif (FABMat03):      codigo = '189'
    elif (FABMat04):      codigo = '190'
    elif (FABMat05):      codigo = '191'
    return (codigo)



def get_MedioComunicacion(codigo) :
    descrip = ""
    if   (codigo == '001') :      descrip = 'Mail'
    elif (codigo == '002') :      descrip = 'Teléfono'
    elif (codigo == '003') :      descrip = 'WhatsApp'
    return (descrip)

def buscarCliente(request, usrid):
    session = getSession(usrid)
    busqueda = request.POST['Busqueda']
    clientesOk = []
    #clientes = Clientes.objects.all().filter(IdUser=usrid)[0:200]
    clientes = Clientes.objects.all().filter()[0:200]
    
    if busqueda:
        clientes = Clientes.objects.filter(
            Q(IdCliente__icontains = busqueda) |
            Q(NombreCliente__icontains = busqueda) |
            Q(RFC__icontains = busqueda) |
            Q(Duns__icontains = busqueda) 
        ).distinct()
    
    for item in clientes.iterator():
        #if(item.IdUser==usrid):
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



def setMaquinasCliente(cliente):
    MarcaArrVir01 = "Dn Solutions"
    MarcaArrVir02 = 'Okuma'
    MarcaArrVir03 = 'Dmg Mori'
    MarcaArrVir04 = 'Mazak'
    MarcaArrVir05 = 'Hision'
    MarcaArrVir06 = 'Hyundai'
    MarcaArrVir07 = 'Baoji'
    MarcaArrVir08 = 'Makino'
    MarcaArrVir09 = 'Romi'
    MarcaArrVir10 = 'Chiron'
    MarcaArrVirOtra = getMarca(cliente.IdCliente, '01', 'Otr')
    ArrVirMarca01 = validMarca(cliente.IdCliente, '01', '01')
    ArrVirMarca02 = validMarca(cliente.IdCliente, '01', '02')
    ArrVirMarca03 = validMarca(cliente.IdCliente, '01', '03')
    ArrVirMarca04 = validMarca(cliente.IdCliente, '01', '04')
    ArrVirMarca05 = validMarca(cliente.IdCliente, '01', '05')
    ArrVirMarca06 = validMarca(cliente.IdCliente, '01', '06')
    ArrVirMarca07 = validMarca(cliente.IdCliente, '01', '07')
    ArrVirMarca08 = validMarca(cliente.IdCliente, '01', '08')
    ArrVirMarca09 = validMarca(cliente.IdCliente, '01', '09')
    ArrVirMarca10 = validMarca(cliente.IdCliente, '01', '10')
    ArrVirMarcaOtra = validMarca(cliente.IdCliente, '01', 'Otr')

    MarcaElectro01 = "Sodick"
    MarcaElectro02 = 'Mitsubishi'
    MarcaElectro03 = 'Shem'
    MarcaElectro04 = 'Accutex'
    MarcaElectro05 = 'Makino'
    MarcaElectro06 = 'Ipretech'
    MarcaElectro07 = 'Mc-Lane'
    MarcaElectro08 = 'Excetek'
    MarcaElectro09 = 'Maincasa'
    MarcaElectro10 = 'Protecnic'
    MarcaElectroOtra = getMarca(cliente.IdCliente, '02', 'Otr')
    ElectroMarca01 = validMarca(cliente.IdCliente, '02', '01')
    ElectroMarca02 = validMarca(cliente.IdCliente, '02', '02')
    ElectroMarca03 = validMarca(cliente.IdCliente, '02', '03')
    ElectroMarca04 = validMarca(cliente.IdCliente, '02', '04')
    ElectroMarca05 = validMarca(cliente.IdCliente, '02', '05')
    ElectroMarca06 = validMarca(cliente.IdCliente, '02', '06')
    ElectroMarca07 = validMarca(cliente.IdCliente, '02', '07')
    ElectroMarca08 = validMarca(cliente.IdCliente, '02', '08')
    ElectroMarca09 = validMarca(cliente.IdCliente, '02', '09')
    ElectroMarca10 = validMarca(cliente.IdCliente, '02', '10')
    ElectroMarcaOtra = validMarca(cliente.IdCliente, '02', 'Otr')

    MarcaInyec01 = "Haitian"
    MarcaInyec02 = 'Engel'
    MarcaInyec03 = 'Sumitomo'
    MarcaInyec04 = 'Krauss Maffei'
    MarcaInyec05 = 'Nissei'
    MarcaInyec06 = 'Borche'
    MarcaInyec07 = 'Arburg'
    MarcaInyec08 = 'CLF'
    MarcaInyec09 = 'Tai-Mex'
    MarcaInyec10 = 'Bole'
    MarcaInyecOtra = getMarca(cliente.IdCliente, '03', 'Otr')
    InyecMarca01 = validMarca(cliente.IdCliente, '03', '01')
    InyecMarca02 = validMarca(cliente.IdCliente, '03', '02')
    InyecMarca03 = validMarca(cliente.IdCliente, '03', '03')
    InyecMarca04 = validMarca(cliente.IdCliente, '03', '04')
    InyecMarca05 = validMarca(cliente.IdCliente, '03', '05')
    InyecMarca06 = validMarca(cliente.IdCliente, '03', '06')
    InyecMarca07 = validMarca(cliente.IdCliente, '03', '07')
    InyecMarca08 = validMarca(cliente.IdCliente, '03', '08')
    InyecMarca09 = validMarca(cliente.IdCliente, '03', '09')
    InyecMarca10 = validMarca(cliente.IdCliente, '03', '10')
    InyecMarcaOtra = validMarca(cliente.IdCliente, '03', 'Otr')

    MarcaLaser01 = "Bodor"
    MarcaLaser02 = 'Gweike'
    MarcaLaser03 = 'Trumpf'
    MarcaLaser04 = 'Bimex'
    MarcaLaser05 = 'Durma'
    MarcaLaser06 = 'Aida'
    MarcaLaser07 = 'Amada'
    MarcaLaser08 = 'JFY'
    MarcaLaser09 = 'Bystronic'
    MarcaLaser10 = 'BLM'
    MarcaLaserOtra = getMarca(cliente.IdCliente, '04', 'Otr')
    LaserMarca01 = validMarca(cliente.IdCliente, '04', '01')
    LaserMarca02 = validMarca(cliente.IdCliente, '04', '02')
    LaserMarca03 = validMarca(cliente.IdCliente, '04', '03')
    LaserMarca04 = validMarca(cliente.IdCliente, '04', '04')
    LaserMarca05 = validMarca(cliente.IdCliente, '04', '05')
    LaserMarca06 = validMarca(cliente.IdCliente, '04', '06')
    LaserMarca07 = validMarca(cliente.IdCliente, '04', '07')
    LaserMarca08 = validMarca(cliente.IdCliente, '04', '08')
    LaserMarca09 = validMarca(cliente.IdCliente, '04', '09')
    LaserMarca10 = validMarca(cliente.IdCliente, '04', '10')
    LaserMarcaOtra = validMarca(cliente.IdCliente, '04', 'Otr')

    MarcaPrensa01 = "Fagor"
    MarcaPrensa02 = 'Aida'
    MarcaPrensa03 = 'Simpac'
    MarcaPrensa04 = 'Shem'
    MarcaPrensa05 = 'Amada'
    MarcaPrensa06 = 'Komatsu'
    MarcaPrensa07 = 'Schuler'
    MarcaPrensa08 = 'Marubeni'
    MarcaPrensa09 = 'Mitsubishi'
    MarcaPrensa10 = 'Seyi'
    MarcaPrensaOtra = getMarca(cliente.IdCliente, '05', 'Otr')
    PrensaMarca01 = validMarca(cliente.IdCliente, '05', '01')
    PrensaMarca02 = validMarca(cliente.IdCliente, '05', '02')
    PrensaMarca03 = validMarca(cliente.IdCliente, '05', '03')
    PrensaMarca04 = validMarca(cliente.IdCliente, '05', '04')
    PrensaMarca05 = validMarca(cliente.IdCliente, '05', '05')
    PrensaMarca06 = validMarca(cliente.IdCliente, '05', '06')
    PrensaMarca07 = validMarca(cliente.IdCliente, '05', '07')
    PrensaMarca08 = validMarca(cliente.IdCliente, '05', '08')
    PrensaMarca09 = validMarca(cliente.IdCliente, '05', '09')
    PrensaMarca10 = validMarca(cliente.IdCliente, '05', '10')
    PrensaMarcaOtra = validMarca(cliente.IdCliente, '05', 'Otr')

    MarcaDoblad01 = "Durma"
    MarcaDoblad02 = 'Amada'
    MarcaDoblad03 = 'Shem'
    MarcaDoblad04 = 'Bystronic'
    MarcaDoblad05 = 'Yawe'
    MarcaDoblad06 = 'Amob'
    MarcaDoblad07 = 'Trumpf'
    MarcaDoblad08 = 'BLM'
    MarcaDoblad09 = 'Nargesa'
    MarcaDoblad10 = 'MVD'
    MarcaDobladOtra = getMarca(cliente.IdCliente, '06', 'Otr')
    DobladMarca01 = validMarca(cliente.IdCliente, '06', '01')
    DobladMarca02 = validMarca(cliente.IdCliente, '06', '02')
    DobladMarca03 = validMarca(cliente.IdCliente, '06', '03')
    DobladMarca04 = validMarca(cliente.IdCliente, '06', '04')
    DobladMarca05 = validMarca(cliente.IdCliente, '06', '05')
    DobladMarca06 = validMarca(cliente.IdCliente, '06', '06')
    DobladMarca07 = validMarca(cliente.IdCliente, '06', '07')
    DobladMarca08 = validMarca(cliente.IdCliente, '06', '08')
    DobladMarca09 = validMarca(cliente.IdCliente, '06', '09')
    DobladMarca10 = validMarca(cliente.IdCliente, '06', '10')
    DobladMarcaOtra = validMarca(cliente.IdCliente, '06', 'Otr')

    maquina = {
        "MarcaArrVir01": MarcaArrVir01,
        "MarcaArrVir02": MarcaArrVir02,
        "MarcaArrVir03": MarcaArrVir03,
        "MarcaArrVir04": MarcaArrVir04,
        "MarcaArrVir05": MarcaArrVir05,
        "MarcaArrVir06": MarcaArrVir06,
        "MarcaArrVir07": MarcaArrVir07,
        "MarcaArrVir08": MarcaArrVir08,
        "MarcaArrVir09": MarcaArrVir09,
        "MarcaArrVir10": MarcaArrVir10,
        "MarcaArrVirOtra": MarcaArrVirOtra,
        "ArrVirMarca01": ArrVirMarca01,
        "ArrVirMarca02": ArrVirMarca02,
        "ArrVirMarca03": ArrVirMarca03,
        "ArrVirMarca04": ArrVirMarca04,
        "ArrVirMarca05": ArrVirMarca05,
        "ArrVirMarca06": ArrVirMarca06,
        "ArrVirMarca07": ArrVirMarca07,
        "ArrVirMarca08": ArrVirMarca08,
        "ArrVirMarca09": ArrVirMarca09,
        "ArrVirMarca10": ArrVirMarca10,
        "ArrVirMarcaOtra": ArrVirMarcaOtra,
        "MarcaElectro01": MarcaElectro01,
        "MarcaElectro02": MarcaElectro02,
        "MarcaElectro03": MarcaElectro03,
        "MarcaElectro04": MarcaElectro04,
        "MarcaElectro05": MarcaElectro05,
        "MarcaElectro06": MarcaElectro06,
        "MarcaElectro07": MarcaElectro07,
        "MarcaElectro08": MarcaElectro08,
        "MarcaElectro09": MarcaElectro09,
        "MarcaElectro10": MarcaElectro10,
        "MarcaElectroOtra": MarcaElectroOtra,
        "ElectroMarca01": ElectroMarca01,
        "ElectroMarca02": ElectroMarca02,
        "ElectroMarca03": ElectroMarca03,
        "ElectroMarca04": ElectroMarca04,
        "ElectroMarca05": ElectroMarca05,
        "ElectroMarca06": ElectroMarca06,
        "ElectroMarca07": ElectroMarca07,
        "ElectroMarca08": ElectroMarca08,
        "ElectroMarca09": ElectroMarca09,
        "ElectroMarca10": ElectroMarca10,
        "ElectroMarcaOtra": ElectroMarcaOtra,
        "MarcaInyec01": MarcaInyec01,
        "MarcaInyec02": MarcaInyec02,
        "MarcaInyec03": MarcaInyec03,
        "MarcaInyec04": MarcaInyec04,
        "MarcaInyec05": MarcaInyec05,
        "MarcaInyec06": MarcaInyec06,
        "MarcaInyec07": MarcaInyec07,
        "MarcaInyec08": MarcaInyec08,
        "MarcaInyec09": MarcaInyec09,
        "MarcaInyec10": MarcaInyec10,
        "MarcaInyecOtra": MarcaInyecOtra,
        "InyecMarca01": InyecMarca01,
        "InyecMarca02": InyecMarca02,
        "InyecMarca03": InyecMarca03,
        "InyecMarca04": InyecMarca04,
        "InyecMarca05": InyecMarca05,
        "InyecMarca06": InyecMarca06,
        "InyecMarca07": InyecMarca07,
        "InyecMarca08": InyecMarca08,
        "InyecMarca09": InyecMarca09,
        "InyecMarca10": InyecMarca10,
        "InyecMarcaOtra": InyecMarcaOtra,
        "MarcaLaser01": MarcaLaser01,
        "MarcaLaser02": MarcaLaser02,
        "MarcaLaser03": MarcaLaser03,
        "MarcaLaser04": MarcaLaser04,
        "MarcaLaser05": MarcaLaser05,
        "MarcaLaser06": MarcaLaser06,
        "MarcaLaser07": MarcaLaser07,
        "MarcaLaser08": MarcaLaser08,
        "MarcaLaser09": MarcaLaser09,
        "MarcaLaser10": MarcaLaser10,
        "MarcaLaserOtra": MarcaLaserOtra,
        "LaserMarca01": LaserMarca01,
        "LaserMarca02": LaserMarca02,
        "LaserMarca03": LaserMarca03,
        "LaserMarca04": LaserMarca04,
        "LaserMarca05": LaserMarca05,
        "LaserMarca06": LaserMarca06,
        "LaserMarca07": LaserMarca07,
        "LaserMarca08": LaserMarca08,
        "LaserMarca09": LaserMarca09,
        "LaserMarca10": LaserMarca10,
        "LaserMarcaOtra": LaserMarcaOtra,
        "MarcaPrensa01": MarcaPrensa01,
        "MarcaPrensa02": MarcaPrensa02,
        "MarcaPrensa03": MarcaPrensa03,
        "MarcaPrensa04": MarcaPrensa04,
        "MarcaPrensa05": MarcaPrensa05,
        "MarcaPrensa06": MarcaPrensa06,
        "MarcaPrensa07": MarcaPrensa07,
        "MarcaPrensa08": MarcaPrensa08,
        "MarcaPrensa09": MarcaPrensa09,
        "MarcaPrensa10": MarcaPrensa10,
        "MarcaPrensaOtra": MarcaPrensaOtra,
        "PrensaMarca01": PrensaMarca01,
        "PrensaMarca02": PrensaMarca02,
        "PrensaMarca03": PrensaMarca03,
        "PrensaMarca04": PrensaMarca04,
        "PrensaMarca05": PrensaMarca05,
        "PrensaMarca06": PrensaMarca06,
        "PrensaMarca07": PrensaMarca07,
        "PrensaMarca08": PrensaMarca08,
        "PrensaMarca09": PrensaMarca09,
        "PrensaMarca10": PrensaMarca10,
        "PrensaMarcaOtra": PrensaMarcaOtra,
        "MarcaDoblad01": MarcaDoblad01,
        "MarcaDoblad02": MarcaDoblad02,
        "MarcaDoblad03": MarcaDoblad03,
        "MarcaDoblad04": MarcaDoblad04,
        "MarcaDoblad05": MarcaDoblad05,
        "MarcaDoblad06": MarcaDoblad06,
        "MarcaDoblad07": MarcaDoblad07,
        "MarcaDoblad08": MarcaDoblad08,
        "MarcaDoblad09": MarcaDoblad09,
        "MarcaDoblad10": MarcaDoblad10,
        "MarcaDobladOtra": MarcaDobladOtra,
        "DobladMarca01": DobladMarca01,
        "DobladMarca02": DobladMarca02,
        "DobladMarca03": DobladMarca03,
        "DobladMarca04": DobladMarca04,
        "DobladMarca05": DobladMarca05,
        "DobladMarca06": DobladMarca06,
        "DobladMarca07": DobladMarca07,
        "DobladMarca08": DobladMarca08,
        "DobladMarca09": DobladMarca09,
        "DobladMarca10": DobladMarca10,
        "DobladMarcaOtra": DobladMarcaOtra,
    }
    return maquina

def setMaterialCliente(cliente): 
    ArrVirMat01 = validMaterial(cliente.IdCliente, '01', '163')
    ArrVirMat02 = validMaterial(cliente.IdCliente, '01', '164')
    ArrVirMat03 = validMaterial(cliente.IdCliente, '01', '165')
    ArrVirMat04 = validMaterial(cliente.IdCliente, '01', '166')
    ArrVirMat05 = validMaterial(cliente.IdCliente, '01', '167')
    ArrVirMat06 = validMaterial(cliente.IdCliente, '01', '168')

    ElectroMat01 = validMaterial(cliente.IdCliente, '02', '170')
    ElectroMat02 = validMaterial(cliente.IdCliente, '02', '171')
    ElectroMat03 = validMaterial(cliente.IdCliente, '02', '172')
    ElectroMat04 = validMaterial(cliente.IdCliente, '02', '173')
    ElectroMat05 = validMaterial(cliente.IdCliente, '02', '174')
    ElectroMat06 = validMaterial(cliente.IdCliente, '02', '175')
    ElectroMat07 = validMaterial(cliente.IdCliente, '02', '176')

    InyecMat01 = validMaterial(cliente.IdCliente, '03', '179')
    InyecMat02 = validMaterial(cliente.IdCliente, '03', '180')
    InyecMat03 = validMaterial(cliente.IdCliente, '03', '181')
    InyecMat04 = validMaterial(cliente.IdCliente, '03', '182')
    InyecMat05 = validMaterial(cliente.IdCliente, '03', '183')
    InyecMat06 = validMaterial(cliente.IdCliente, '03', '184')
    InyecMat07 = validMaterial(cliente.IdCliente, '03', '185')

    FABMat01 = validMaterial(cliente.IdCliente, '04', '187')
    FABMat02 = validMaterial(cliente.IdCliente, '04', '188')
    FABMat03 = validMaterial(cliente.IdCliente, '04', '189')
    FABMat04 = validMaterial(cliente.IdCliente, '04', '190')
    FABMat05 = validMaterial(cliente.IdCliente, '04', '191')

    material = {
        "ArrVirMat01": ArrVirMat01,
        "ArrVirMat02": ArrVirMat02,
        "ArrVirMat03": ArrVirMat03,
        "ArrVirMat04": ArrVirMat04,
        "ArrVirMat05": ArrVirMat05,
        "ArrVirMat06": ArrVirMat06,
        "ElectroMat01": ElectroMat01,
        "ElectroMat02": ElectroMat02,
        "ElectroMat03": ElectroMat03,
        "ElectroMat04": ElectroMat04,
        "ElectroMat05": ElectroMat05,
        "ElectroMat06": ElectroMat06,
        "ElectroMat07": ElectroMat07,
        "InyecMat01": InyecMat01,
        "InyecMat02": InyecMat02,
        "InyecMat03": InyecMat03,
        "InyecMat04": InyecMat04,
        "InyecMat05": InyecMat05,
        "InyecMat06": InyecMat06,
        "InyecMat07": InyecMat07,
        "FABMat01": FABMat01,
        "FABMat02": FABMat02,
        "FABMat03": FABMat03,
        "FABMat04": FABMat04,
        "FABMat05": FABMat05
    }
    return material

