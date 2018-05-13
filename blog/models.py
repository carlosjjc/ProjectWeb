from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from decimal import Decimal

"""
class Post(models.Model):
    author = models.ForeignKey('auth.User',on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True,null = True)
    
    def publish(self):
        self.published_date = timezone.now()
        self.save()
        
    def __str__(self):
        return self.title
"""


class Jogador(models.Model):
    id = models.OneToOneField(User, primary_key=True,on_delete=models.CASCADE, blank=False, null=False)
    """nome = models.CharField(max_length=200)
    usuario = models.EmailField(max_length=100,unique=True)
    senha = models.CharField(max_length=200)"""
    saldo = models.DecimalField(max_digits=10,decimal_places=2,default=10.00)
    
    def getSaldo(self):
        return self.saldo
    
    def __str__(self):
        return str(self.id)
    
class Time(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=200,unique=True)
    
    def __str__(self):
        return self.nome

class Partida(models.Model):
    id = models.AutoField(primary_key=True)
    time_casa = models.ForeignKey(Time,related_name='time1',on_delete=models.CASCADE)
    time_visitante = models.ForeignKey(Time,related_name='time2',on_delete=models.CASCADE)
    data = models.DateField(blank=True,null=True)
    #gol_casa = models.IntegerField(default=0,blank=False,null=False)
    #gol_visitante = models.IntegerField(default=0,blank=False,null=False)
    
    def __str__(self):
        return str(self.time_casa) + " x " + str(self.time_visitante) +" ("+ str(self.data)+")"

    def getTimeCasa(self):
        return str(self.time_casa)

    """def getGolsCasa(self):
        return str(self.gols_casa)"""

    def getTimeVisitante(self):
        return str(self.time_visitante)

    """def getGolsVisitante(self):
        return str(self.gols_visitante)"""
    
    """def getPlacar(self):
        return str(self.time_casa) + "" + str(self.gols_casa) + " x " + str(self.gols_time_visitante) + "" + str(self.time_visitante) """
    
class Resultado(models.Model):
    id = models.AutoField(primary_key=True)
    id_partida = models.OneToOneField(Partida,blank=False,null=False)
    gols_time_casa = models.IntegerField(default=0,blank=False,null=False)
    gols_time_visitante = models.IntegerField(default=0,blank=False,null=False)
    
    def __str__(self):
        return str(self.id_partida) + ": "+str (self.gols_time_casa) + " X " + str(self.gols_time_visitante)


class Aposta(models.Model):
    id = models.AutoField(primary_key=True)
    id_jogador = models.ForeignKey(Jogador,blank=False,null=False, on_delete=models.CASCADE)
    id_partida = models.ForeignKey(Partida,blank=False,null=False,on_delete=models.CASCADE)
    gols_time_casa = models.IntegerField(default=0, blank=False, null=False)
    gols_time_visitante = models.IntegerField(default=0, blank=False, null=False)
    data = models.DateField(default=timezone.now)
    #valor = models.DecimalField(max_digits=10, decimal_places=2,default=5.0,blank=False,null=False) 
    
    def __str__(self):
        return str(self.id_jogador)+ ". "+str(self.id_partida) + ": " + str(self.gols_time_casa) + " X " + str(self.gols_time_visitante)

@receiver(post_save, sender=Resultado)
def resultado_partida_trigger(sender,instance, **kwargs):
    apostas = Aposta.objects.filter(id_partida=instance.id_partida)
    vencedores = []
    for aposta in apostas:
        if aposta.gols_time_casa == instance.gols_time_casa and aposta.gols_time_visitante == instance.gols_time_visitante:
            vencedores.append(aposta.id_jogador)
            print(vencedores)
    
    if not vencedores:
        for aposta in apostas:
            if instance.gols_time_casa > instance.gols_time_visitante:
                if aposta.gols_time_casa > aposta.gols_time_visitante:
                    vencedores.append(aposta.id_jogador)
            elif instance.gols_time_casa < instance.gols_time_visitante:
                if aposta.gols_time_casa < aposta.gols_time_visitante:
                    vencedores.append(aposta.id_jogador)
            else:
                if aposta.gols_time_casa == aposta.gols_time_visitante:
                    vencedores.append(aposta.id_jogador)
        print('Segundo For',vencedores)
    
    valor = 5
    
    if not vencedores:
        for aposta in apostas:
            vencedores.append(aposta.id_jogador)
            
    numVencedores = len(vencedores)
    valor = len(apostas)*5 / numVencedores
    print(valor)
    
    for vencedor in vencedores:    
        saldo = vencedor.saldo
        add_saldo = saldo + Decimal(valor)
        vencedor.saldo = add_saldo
        vencedor.save()

                
