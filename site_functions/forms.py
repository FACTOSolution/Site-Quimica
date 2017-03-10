from django import forms
from .models import *
from localflavor.br import forms as fm


class UserForm(forms.ModelForm):   
	choices = ( 
		(1,'Sim'),
		(0,'Não'),
 	)

	have_article = forms.TypedChoiceField(label='Vai enviar trabalho?',
						 choices=choices, widget=forms.RadioSelect, coerce=int
					)
	password = forms.CharField(label=("Senha"), widget=forms.PasswordInput(attrs={'placeholder' : 'Digite sua senha.'}))
	name = forms.CharField(label='Nome')
	instituicao = forms.CharField(label='Instituição')
	cpf = fm.BRCPFField(label='CPF')
	phone = forms.CharField(label='Telefone')
	class Meta:
		model = UserProfile
		fields = ('name','instituicao', 'cpf','phone','password','email','modalidade','minicursos','have_article',)
		widgets = {
			'minicursos': forms.CheckboxSelectMultiple(),
		}

class ReceiptForm(forms.Form):
	image_file = forms.ImageField()
	user_id = forms.IntegerField()

class ArticleForm(forms.ModelForm):
	class Meta:
		model = Article
		fields = ('title', 'document')