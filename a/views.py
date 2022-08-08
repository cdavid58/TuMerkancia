from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import * 
from datetime import date
from datetime import datetime

def masVendido():
	masV = MasVendido.objects.all().order_by('-cantidad')
	dato = []
	for i in masV:
		if int(i.cantidad) > 20:
			dato.append(i)
	return dato

def salir(request):
	cart = Carrito(request)
	if len(cart) > 0:
		cart.clear()
	request.session['carrito'] = 0
	del request.session['usuario']
	return redirect('home')

def login(request):
	error = False
	if request.method == 'POST':
		try:
			print(request.POST.get('telefono'))
			cliente = Cliente.objects.get(telefono=str(request.POST.get('telefono')))
		except Cliente.DoesNotExist:
			cliente = None

		if cliente is not None:
			request.session['usuario'] = str(request.POST.get('telefono'))
			return redirect('home')
		else:
			error = True
			
	return render(request,'login.html',{'error':error})

def detalleCarrito(request):
	lista = []
	if 'carrito' in request.session:
		print(lista,'Lista')
		cart = Carrito(request)		
		if len(cart) > 0:
			for i in cart:
				print(i['cantidad'])
				lista.append({'nombre':i['articulo'],'precio':i['total'],'cantidad':i['cantidad'],'imagen':i['img']})
			print(lista,'Lista_2')
			return lista
	return lista

def home(request):
	if 'carrito' not in request.session:
		request.session['carrito'] = 0

	categorias = Categoria.objects.all()
	producto_portada = Producto.objects.filter(pordata=True)

	return  render(request,'index.html',{'categorias':categorias,'producto':producto_portada,'cartshopping':detalleCarrito(request),'mv':masVendido()})


def Lista_Productos(request,pk):

	if int(pk) == 0:
		categorias = Categoria.objects.all()
		producto = Producto.objects.all()
		return render(request,'product.html',{'categorias':categorias,'producto':producto,'cat':'Todas','mv':masVendido()})

	else:
		categorias = Categoria.objects.all()
		cat = Categoria.objects.get(pk=pk)
		producto = Producto.objects.filter(categoria=cat)
		return render(request,'product.html',{'categorias':categorias,'producto':producto,'cat':cat,'mv':masVendido()})


def Products_Single(request,pk):
	if request.is_ajax():
		add_cart(request,int(request.GET.get('producto')), request.GET.get('cantidad'))

		return HttpResponse(request.session['carrito'])

	producto = Producto.objects.get(pk=pk)
	categorias = Categoria.objects.all()

	return render(request,'product-single.html',{'categorias':categorias,'producto':producto,'cartshopping':detalleCarrito(request)})


def CartShopping(request):
	categorias = Categoria.objects.all()
	cart = Carrito(request)
	if request.is_ajax():
		cart_remove(request,int(request.GET.get('id')))
		return HttpResponse('')

	subtotal = 0
	
	for i in cart:
		subtotal += float(i['total'])
	domi = 5000 if subtotal != 0 else 0
	total = subtotal + domi


	return render(request,'cart.html',{'cart':cart,'total':total,'subtotal':subtotal,'domi':domi,'categorias':categorias})

def Checkout(request):
	cart = Carrito(request)
	subtotal = 0
	for i in cart:
		subtotal += float(i['total'])
	domi = 5000 if subtotal != 0 else 0
	total = subtotal + domi

	if request.method == 'POST':
		now = datetime.now()
		con = Consecutivo.objects.get(pk=1)
		try:
			cliente = Cliente.objects.get(telefono=request.POST.get('telefono'))
		except Cliente.DoesNotExist:
			cliente = None
			Cliente(
				nombre = request.POST.get('name'),
				apellido = request.POST.get('ape'),
				direccion = request.POST.get('direc'),
				opcional = request.POST.get('opcional'),
				telefono = request.POST.get('telefono'),
				email = request.POST.get('email')
			).save()
		if 'usuario' not in request.session:
			request.session['usuario'] = str(request.POST.get('telefono'))

		for i in cart:
			print('Entre')
			Pedido(
				conse = con,
				codigo = i['codigo'],
				articulo = i['articulo'],
				cantidad = i['cantidad'],
				precio = i['precio'],
				fecha = date.today(),
				hora = str(now.hour) +':'+ str(now.minute),
				cliente = cliente if cliente is not None else Cliente.objects.get(telefono=request.POST.get('telefono')),
				direccion = Cliente.objects.get(telefono=request.POST.get('telefono')).direccion if request.POST.get('otra') != 'on' else "Otra direccion"
			).save()

			try:
				print('try')
				mv = MasVendido.objects.get(cliente=Cliente.objects.get(telefono=request.POST.get('telefono')),producto=Producto.objects.get(pk=i['codigo']))
			except MasVendido.DoesNotExist:
				mv = None


			if mv is not None:
				print('if')
				cnt = int(mv.cantidad) + int(i['cantidad'])
				mv.cantidad = cnt
				mv.save()

			else:
				print('else')
				MasVendido(
					cliente = Cliente.objects.get(telefono=request.POST.get('telefono')),
					producto = Producto.objects.get(pk=i['codigo']),
					cantidad = i['cantidad']
				).save()

		n = int(con.numero) + 1
		con.numero = n
		con.save()
		print('Ya guarde')

		return redirect('/Invoice/')

	categorias = Categoria.objects.all()
	return render(request,'checkout.html',{'total':total,'subtotal':subtotal,'domi':domi,'categorias':categorias})


def Invoice(request):
	cart = Carrito(request)
	categorias = Categoria.objects.all()
	if len(cart) > 0:
		subtotal = 0
		fp = "Efectivo"
		for j in cart:
			subtotal += float(j['total'])
		total = subtotal + 5000
		carr = cart
		cart.clear()
		return render(request,'invoice.html',{'total':total,'subtotal':subtotal,'domi':5000,'categorias':categorias,
													'fecha':date.today(),'fp':fp,'carrito':carr
												})

	return redirect('CartShopping')

def add_cart(request,pk,cantidad):
	producto = Producto.objects.get(pk=pk)
	cart = Carrito(request)
	cart.add(producto,int(cantidad))


def cart_remove(request,pk):
	cart = Carrito(request)
	product = Producto.objects.get(pk=pk)
	cart.remove(product)
	resta = int(request.session['carrito']) - 1
	request.session['carrito'] = resta