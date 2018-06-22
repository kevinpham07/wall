from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name = "index"),
	url(r'register/$', views.register, name = "register"),
	url(r'login/$', views.login, name = "login"),
	url(r'wall/$', views.simplewall, name = "wall"),
	url(r'message/$', views.message, name = "message"),
	url(r'comment/$', views.comment, name = "comment"),
	url(r'logout/$', views.logout, name = "logout")
]