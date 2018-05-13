# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.contrib.auth.models import User
from django import forms
from .models import *

class ApostaForm(ModelForm):
    class Meta:
        model = Aposta
        fields = ('id_partida','gols_time_casa','gols_time_visitante')

class UserModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password']
        widgets = {
            'first_name':forms.TextInput(attrs={'class':'form-control','maxlength':255}),
            'last_name':forms.TextInput(attrs={'class':'form-control','maxlength':255}),
            'email':forms.TextInput(attrs={'class':'form-control','maxlength':255}),
            'username':forms.TextInput(attrs={'class':'form-control','maxlength':255}),
            'password':forms.PasswordInput(attrs={'class':'form-control','maxlength':255}),
        }
        
        error_messages = {
            'first_name':{
                    'required': 'Este campo é obrigatorio'
            },
            'last_name':{
                    'required': 'Este campo é obrigatorio'
            },
            'email':{
                    'required': 'Digite um email valido'
            },
            'username':{
                    'required': 'Este campo é obrigatorio'
            },
            'password':{
                    'required': 'Este campo é obrigatorio'
            },
            
        }
            
        def save(self,commit=True):
            user = super(UserModelForm,self).save(commit=False)
            user.set_password(self.cleaned_data['password'])
            if commit:
                user.save()
            return user
