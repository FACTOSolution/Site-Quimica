# -*- coding: utf-8 -*-
from django import forms
from .models import *
from localflavor.br import forms as fm


class UserForm(forms.ModelForm):
	choices = (
		(1,'Sim'),
		(0,'Nao'),
 	)

	have_article = forms.TypedChoiceField(label='Vai enviar trabalho?',
						 choices=choices, widget=forms.RadioSelect, coerce=int
					)
	## MUDANÇAS FEITAS POR MIM(KÁSSIO)##
		#atribui as classes para cada campo do formulário
		#assim todos os campos estão estilizados com o tema do bootstrap
	#adicionei o parametro com a Classe form-control
	password = forms.CharField(label=("Senha"), widget=forms.PasswordInput(attrs={'placeholder' : 'Digite sua senha.', 'class' : 'form-control'}))
	#adicionei o parametro com a Classe form-control
	name = forms.CharField(label='Nome', widget=forms.TextInput(attrs={'class' : 'form-control'}))
	#adicionei o parametro com a Classe form-control
	instituicao = forms.CharField(label='Instituicao', widget=forms.TextInput(attrs={'class' : 'form-control'}))
	#adicionei o parametro com a Classe form-control
	cpf = fm.BRCPFField(label='CPF', widget=forms.TextInput(attrs={'class' : 'form-control'}))
	#adicionei o parametro com a Classe form-control
	phone = forms.CharField(label='Telefone', widget=forms.TextInput(attrs={'class' : 'form-control'}))
	#adicionei essa linha de EMAIL
	email = forms.EmailField(widget=forms.TextInput(attrs={'class' : 'form-control'}))
	#adicionei essa linha com as MODALIDADES
	modalidade = forms.ChoiceField(choices=UserProfile.MODALIDADE_CHOICES, widget=forms.Select(attrs={'class' : 'form-control'}))

	class Meta:
		model = UserProfile
		fields = ('name','instituicao', 'cpf','phone','password','email','modalidade','have_article',)
		widgets = {
			'minicursos': forms.CheckboxSelectMultiple(),
		}

class AdminForm(forms.ModelForm):

	password = forms.CharField(label=("Senha"), widget=forms.PasswordInput(attrs={'placeholder' : 'Digite sua senha.'}))
	name = forms.CharField(label='Nome')
	phone = forms.CharField(label='Telefone')
	class Meta:
		model = UserProfile
		fields = ('name','email','phone','password',)

class ReceiptForm(forms.Form):
	image_file = forms.ImageField()
	user_id = forms.IntegerField()

class ArticleForm(forms.ModelForm):
	title = forms.CharField(label=("Titulo do artigo"))
	document = forms.FileField(label="Arquivo")
	autores = forms.CharField(label="Autores", widget=forms.Textarea( attrs={'placeholder': 'Digite o nome dos autores separados por ponto e virgula em ordem de importância.'}))

	class Meta:
		model = Article
		fields = ('title', 'area', 'autores', 'document',)

class ShortCourseForm(forms.ModelForm):
	class Meta:
		model = Minicurso
		fields = ('name','description','professor','begin','duration')

class ArticleAnalisyForm(forms.Form):
	revision = forms.CharField(widget=forms.Textarea)
	accepted = forms.BooleanField()
