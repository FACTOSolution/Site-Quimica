from django import forms
from .models import *
from localflavor.br import forms as fm


class UserForm(forms.ModelForm):   
	class Meta:
		model = UserProfile
		fields = ('name','instituicao', 'cpf','phone','password','email','modalidade',)
		widgets = {
			'password': forms.PasswordInput(),
			#'cpf': fm.BRCPFField(),
			#'phone': fm.BRPhoneNumberField(),
		}