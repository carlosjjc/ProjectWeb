from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.initialize,name='initialize'),
    url(r'^home/$',views.initialize,name='initialize'),
    url(r'^cadastro/$',views.cadastro, name='cadastro'),
    url(r'^login/$',views.autenticar, name='autenticar'),
    url(r'^deslogar/$',views.deslogar, name='deslogar'),
    url(r'^ranking/$',views.ranking,name='ranking'),
    url(r'^apostar/$',views.apostar,name='apostar'),
    url(r'^resultados/$',views.resultado,name='resultado'),
    url(r'^partida/(?P<pk>[0-9]+)/$', views.apostar, name= 'time_detail'),
]
