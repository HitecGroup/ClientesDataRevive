from django.db import models

# Create your models here.
class Clientes(models.Model):
    IdCliente=models.CharField(primary_key=True,max_length=20)
    NombreCliente=models.CharField(max_length=50)
    DireccioCliente=models.CharField(max_length=150)
    ClaveExterna=models.CharField(max_length=16,default="0000000000")
    TelefonoPrincipal=models.CharField(max_length=12,default="5555555555")
    RFC=models.CharField(max_length=13,default="XAXX010101000")
    TipoCliente=models.CharField(max_length=50,default="Coorporativo")
    ClientePotencial=models.BooleanField(default=False)
    Duns=models.CharField(max_length=18,default="ABCDEFGHIJKL-DUNS")
    NombreAdicional=models.CharField(max_length=50,default="Sin Adicional")
    Sector=models.CharField(max_length=50,default="Customer Service")
    FechaNacimiento=models.DateField(default="2023-09-01")
    Clasificacion=models.CharField(max_length=15,default="PA")
    Estado=models.BooleanField(default=True)
    Division=models.CharField(max_length=60,default="HAAS")
    SucServicio=models.CharField(max_length=50,default="Defualt")
    TipoEmpresa=models.CharField(max_length=50,default="Sin Especificar")
    NoTurnosC=models.CharField(max_length=15,default="Sin Turnos")
    NoMaqConvenC=models.CharField(max_length=15,default="Sin Turnos")
    NoMaqCNC_C=models.CharField(max_length=15,default="Sin Turnos")
    Tier=models.CharField(max_length=50,default="Sin Especificar")
    NoMaqHT_C=models.CharField(max_length=15,default="Sin Turnos")
    MatUseCHMER=models.CharField(max_length=50,default="Varios 2")
    MatUseYIZUMI=models.CharField(max_length=50,default="Varios 2")
    FrecuenciaCompra=models.CharField(max_length=50,default="Varios 2")
    ActPriEDM=models.CharField(max_length=50,default="Varios 2")
    DivisionPM=models.CharField(max_length=50,default="Varios 2")
    RegionVts=models.CharField(max_length=50,default="Varios 2")
    ActPriEquipo=models.CharField(max_length=50,default="Varios 2")
    ActPriFAB=models.CharField(max_length=50,default="Varios 2")
    MatUsoCNC_Haas=models.CharField(max_length=50,default="Varios 2")
    MatUsoFab=models.CharField(max_length=50,default="Varios 2")
    subDivision=models.CharField(max_length=40,default="Varios 2")
    iDNielsen=models.CharField(max_length=40,default="Varios 2")
    ActPriEquipoCNC=models.CharField(max_length=40,default="Varios 2")
    MatViruta=models.CharField(max_length=40,default="Varios 2")


    def __str__(self):
        texto = "{0} ({1})"
        return texto.format(self.IdCliente,
                            self.NombreCliente,
                            self.DireccioCliente,
                            self.ClaveExterna,
                            self.TelefonoPrincipal,
                            self.RFC,
                            self.TipoCliente,
                            self.ClientePotencial,
                            self.Duns,
                            self.NombreAdicional,
                            self.Sector,
                            self.FechaNacimiento,
                            self.Clasificacion,
                            self.Estado,
                            self.Division,
                            self.SucServicio,
                            self.TipoEmpresa,
                            self.NoTurnosC,
                            self.NoMaqConvenC,
                            self.NoMaqCNC_C,
                            self.Tier,
                            self.NoMaqHT_C,
                            self.MatUseCHMER,
                            self.MatUseYIZUMI,
                            self.FrecuenciaCompra,
                            self.ActPriEDM,
                            self.DivisionPM,
                            self.RegionVts,
                            self.ActPriEquipo,
                            self.ActPriFAB,
                            self.MatUsoCNC_Haas,
                            self.MatUsoFab,
                            self.subDivision,
                            self.iDNielsen,
                            self.ActPriEquipoCNC,
                            self.MatViruta
)

class Contactos(models.Model):
    IdCliente=models.CharField(max_length=80,default="Sin Dato")
    IdContacto=models.CharField(primary_key=True,max_length=80,default="0000000")
    Nombre=models.CharField(max_length=40,default="Sin Dato")
    SegundoNombre=models.CharField(max_length=40,default="Sin Dato")
    Apellidos=models.CharField(max_length=100,default="Sin Dato")
    Principal=models.BooleanField(default=False)
    CorreoElectronico=models.CharField(max_length=400,default="mail@hitec.com")
    Telefono=models.CharField(max_length=40,default="Sin Dato")
    TelefonoMovil=models.CharField(max_length=40,default="Sin Dato")
    Vip=models.CharField(max_length=80,default="Sin Dato")
    Funcion=models.CharField(max_length=80,default="Sin Dato")
    Departamento=models.CharField(max_length=80,default="Sin Dato")
    PaisRegion=models.CharField(max_length=80,default="Sin Dato")
    Numero=models.CharField(max_length=80,default="Sin Dato")
    Calle=models.CharField(max_length=60,default="Sin Dato")
    Ciudad=models.CharField(max_length=40,default="Sin Dato")
    Estado=models.CharField(max_length=80,default="Sin Dato")
    CodigoPostal=models.CharField(max_length=10,default="Sin Dato")
    Distrito=models.CharField(max_length=40,default="Sin Dato")
    Edificio=models.CharField(max_length=10,default="Sin Dato")
    Planta=models.CharField(max_length=10,default="Sin Dato")
    PaisExp=models.CharField(max_length=40,default="Sin Dato")
    MedioComunicacion=models.CharField(max_length=30,default="mail@hitec.com")
    RFC=models.CharField(max_length=60,default="XAXX010101000")

    def __str__(self):
        texto = "{0} ({1})"
        return texto.format(self.IdCliente,
                            self.IdContacto,
                            self.Nombre,
                            self.SegundoNombre,
                            self.Apellidos,
                            self.Principal,
                            self.CorreoElectronico,
                            self.Telefono,
                            self.TelefonoMovil,
                            self.Vip,
                            self.Funcion,
                            self.Departamento,
                            self.PaisRegion,
                            self.Numero,
                            self.Calle,
                            self.Ciudad,
                            self.Estado,
                            self.CodigoPostal,
                            self.Distrito,
                            self.Edificio,
                            self.Planta,
                            self.PaisExp,
                            self.MedioComunicacion
                            )

class Direcciones(models.Model):
    IdRegistro=models.AutoField(primary_key=True)
    IdCliente=models.CharField(max_length=50,default="00000000")
    PaisRegion=models.CharField(max_length=80,default="Sin Dato")
    Calle=models.CharField(max_length=60,default="Sin Dato")
    Numero=models.CharField(max_length=10,default="Sin Dato")
    Calle2=models.CharField(max_length=40,default="Sin Dato")
    Ciudad=models.CharField(max_length=40,default="Sin Dato")
    Estado=models.CharField(max_length=80,default="Sin Dato")
    CodigoPostal=models.CharField(max_length=10,default="Sin Dato")
    Distrito=models.CharField(max_length=40,default="Sin Dato")
    CodigoDomFiscal=models.CharField(max_length=80,default="Sin Dato")
    DireccionPrincipal=models.CharField(max_length=1,default="X")
    Entrega=models.CharField(max_length=1,default="X")
    DestinatarioMercEstandar=models.CharField(max_length=1,default="X")
    DestinatarioFactura=models.CharField(max_length=1,default="X")
    Telefono=models.CharField(max_length=40,default="Sin Dato")
    CorreoElectronico=models.CharField(max_length=500,default="Sin Dato")
    SitioWeb=models.CharField(max_length=500,default="Sin Dato")
    

    def __str__(self):
        texto = "{0} ({1})"
        return texto.format(self.IdRegistro,
                            self.IdCliente,
                            self.PaisRegion,
                            self.Calle,
                            self.Numero,
                            self.Calle2,
                            self.Ciudad,
                            self.Estado,
                            self.CodigoPostal,
                            self.Distrito,
                            self.CodigoDomFiscal,
                            self.DireccionPrincipal,
                            self.Entrega,
                            self.DestinatarioMercEstandar,
                            self.DestinatarioFactura,
                            self.Telefono,
                            self.CorreoElectronico,
                            self.SitioWeb)

class Country(models.Model):
    CodeId=models.CharField(primary_key=True,max_length=2)
    Descrip=models.CharField(max_length=50, blank=False)
    
    def __str__(self):
        texto = "{0} ({1})"
        return texto.format(self.CodeId,
                            self.Descrip )
    
class Region(models.Model):
    IdCountry=models.CharField(max_length=2, blank=False)
    CodeId=models.CharField(max_length=3, blank=False)
    Descrip=models.CharField(max_length=20, blank=False)

    def __str__(self):
        texto = "{0} ({1})"
        return texto.format(self.IdCountry,
                            self.CodeId,
                             self.Descrip )
    
class Sepomex(models.Model):
    Id=models.AutoField(primary_key=True)
    D_codigo=models.CharField(max_length=10, blank=False)
    D_asenta=models.CharField(max_length=60, blank=False)
    D_tipo_asenta=models.CharField(max_length=25, blank=False)
    D_mnpio=models.CharField(max_length=50, blank=False)
    D_estado=models.CharField(max_length=35, blank=False)
    D_ciudad=models.CharField(max_length=50, blank=True)
    D_CP=models.CharField(max_length=10, blank=True)
    C_estado=models.IntegerField(null=True)
    D_oficina=models.CharField(max_length=10, blank=True)
    C_CP=models.CharField(max_length=10, blank=True)
    C_tipo_asenta=models.IntegerField(null=False)
    C_mnpio=models.IntegerField(null=False)
    Id_asenta_opcons=models.IntegerField(null=False)
    D_zona=models.CharField(max_length=10, blank=True)
    C_cve_ciudad=models.IntegerField(null=True)

    def __str__(self):
        texto = "{0} ({1})"
        return texto.format(self.Id,
                            self.D_codigo,
                            self.D_asenta,
                            self.D_tipo_asenta,
                            self.D_mnpio,
                            self.D_estado,
                            self.D_ciudad,
                            self.D_CP,
                            self.C_estado,
                            self.D_oficina,
                            self.C_CP,
                            self.C_tipo_asenta,
                            self.C_mnpio,
                            self.Id_asenta_opcons,
                            self.D_zona,
                            self.C_cve_ciudad )
    
class RelReg_Edo(models.Model):
    c_estado=models.IntegerField(null=False)
    idRegion=models.CharField(max_length=3, blank=False)

    def __str__(self):
        texto = "{0} ({1})"
        return texto.format(self.c_estado,
                            self.idRegion )
 