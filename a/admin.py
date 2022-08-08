from django.contrib import admin
from .models import *

admin.site.register(Producto)
admin.site.register(Categoria)
admin.site.register(Consecutivo)
admin.site.register(Pedido)
admin.site.register(Cliente)
admin.site.register(MasVendido)


