from django.contrib import admin
from .models import Clientes
from .models import Contactos
from .models import Direcciones
from .models import Sepomex
from .models import Region
from .models import RelReg_Edo
from .models import Country
from .models import divisionCliente
from .models import Users
from .models import Log
# Register your models here.

admin.site.register(Clientes)
admin.site.register(Contactos)
admin.site.register(Direcciones)
admin.site.register(Sepomex)
admin.site.register(Region)
admin.site.register(RelReg_Edo)
admin.site.register(Country)
admin.site.register(divisionCliente)
admin.site.register(Users)
admin.site.register(Log)
