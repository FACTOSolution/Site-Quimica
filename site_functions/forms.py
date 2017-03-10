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

	class Meta:
		model = UserProfile
		fields = ('name','instituicao', 'cpf','phone','password','email','modalidade','minicursos','have_article',)
		widgets = {
			'password': forms.PasswordInput(),
			'minicursos': forms.CheckboxSelectMultiple(),
			#'have_article': forms.RadioSelect(),
			#'cpf': fm.BRCPFField(),
			#'phone': fm.BRPhoneNumberField(),
		}

class ReceiptForm(forms.Form):
	image_file = forms.ImageField()
	user_id = forms.IntegerField()

class ArticleForm(forms.ModelForm):
	class Meta:
		model = Article
		fields = ('title', 'document')