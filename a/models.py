from django.db import models
from django.http import HttpResponseRedirect
from decimal import Decimal
from django.conf import settings


class Categoria(models.Model):
	name = models.CharField(max_length=50)
	imagen = models.ImageField(upload_to="Categoria")

	def __str__(self):
		return self.name


class Producto(models.Model):
	name = models.CharField(max_length=50)
	cantidad = models.CharField(max_length=10)
	precio = models.CharField(max_length=10)
	pordata = models.BooleanField(default=False)
	imagen = models.ImageField(upload_to="Licores")
	categoria = models.ForeignKey(Categoria,on_delete=models.CASCADE)
	descuento = models.CharField(max_length=3,default=0)
	nuevo = models.BooleanField(default=False)


	def __str__(self):
		return self.name

	def totalDescuento(self):
		return float(self.precio) - float(float(self.precio) * (float(self.descuento) / 100 ))

class MasVendido(models.Model):
	cliente = models.ForeignKey('Cliente',on_delete=models.CASCADE)
	producto = models.ForeignKey(Producto,on_delete=models.CASCADE)
	cantidad = models.CharField(max_length=100)
	mv = []

	def __str__(self):
		return self.producto.name

	def masVendido(self):
		mv = []
		if mv:
			if int(mv[0]['cant']) < int(self.cantidad):
				mv.pop(0)
				mv.append({'id':self.id,'cant':self.cantidad})
		else:
			if int(self.cantidad) > 20:
				mv.append({'id':self.id,'cant':self.cantidad})

		return mv



class Cliente(models.Model):
	nombre = models.CharField(max_length=20)
	apellido = models.CharField(max_length=20)
	direccion = models.TextField()
	opcional = models.TextField(default="")
	telefono = models.CharField(max_length=10)
	email = models.EmailField()

	def __str__(self):
		return self.nombre + ' ' + self.apellido

class Consecutivo(models.Model):
	numero = models.CharField(max_length=20)

	def __str__(self):
		return self.numero


class Pedido(models.Model):
	conse = models.ForeignKey(Consecutivo,on_delete=models.CASCADE)
	codigo = models.CharField(max_length=20)
	articulo = models.CharField(max_length=50)
	cantidad = models.CharField(max_length=20)
	precio = models.CharField(max_length=20)
	fecha = models.CharField(max_length=10)
	hora = models.CharField(max_length=10)
	cliente = models.ForeignKey(Cliente,on_delete=models.CASCADE)
	direccion = models.TextField(default="")
	descuento_producto = models.CharField(max_length=20,default=0)
	descuento_total = models.CharField(max_length=20,default=0)
	entregado = models.BooleanField(default=False)
	domicilio = models.CharField(max_length=7,default=5000)

	def __str__(self):
		return self.conse.numero








class Carrito(object):
	def __init__(self,request):
		self.session = request.session
		cart = self.session.get(settings.CART_SESSION_ID)
		if not cart:
			cart = self.session[settings.CART_SESSION_ID] = {}
		self.cart = cart
		self.request = request

	def save(self):
		self.session[settings.CART_SESSION_ID]=self.cart
		self.session.modified = True

	def add(self,producto,cantidad = 0):
		if str(producto.pk) in self.cart:
			cnt = self.cart[str(producto.pk)]
			t = float(producto.precio) * float(cantidad)
			cnt['total'] = t
			cnt['cantidad'] = cantidad
			self.save()
			print(self.cart)
		else:
			total = float(producto.precio) * float(cantidad)
			self.request.session['carrito'] += 1
			self.cart[str(producto.pk)] = {'codigo':producto.pk,'articulo':producto.name,'cantidad':cantidad,'precio':producto.precio,'total':total,'img':producto.imagen.url}
			print(self.cart)

	def remove(self,product):
		product_id = str(product.pk)
		if product_id in self.cart:
			del self.cart[product_id]
			self.save()

	def __iter__(self):
		print(self.cart)
		product_ids = self.cart.keys()
		products = Producto.objects.filter(id__in=product_ids)
		# for product in products:
		# 	self.cart[str(product.id)]['product']=product

		for item in self.cart.values():
			item['precio']=float(item['precio'])
			item['total']=item['precio']*item['cantidad']
			yield item


	def __len__(self):
		return sum(item['cantidad'] for item in self.cart.values())

	def clear(self):
		del self.session[settings.CART_SESSION_ID]
		self.request.session['carrito'] = 0
		self.session.modified = True
