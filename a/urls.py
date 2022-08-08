from django.conf.urls import url
from .views import *

urlpatterns=[
	
	url(r'^$',home,name="home"),
	url(r'^Lista_Productos/(\d+)/$',Lista_Productos,name="Lista_Productos"),
	url(r'^Products_Single/(\d+)/$',Products_Single,name="Products_Single"),
	url(r'^CartShopping/$',CartShopping,name="CartShopping"),
	url(r'^Checkout/$',Checkout,name="Checkout"),
	url(r'^Invoice/$',Invoice,name="Invoice"),

	url(r'^login/$',login,name="login"),
	url(r'^salir/$',salir,name="salir"),
		
]