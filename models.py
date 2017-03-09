from django.db import models

class Minicurso (models.Model):
	mini_id = models.IntegerField()
	name = models.CharField(max_length=100)
	description = models.TextField(max_length=400)
	professor = models.CharField(max_length=100)
	begin = models.DateTimeField()
	duration = models.DurationField()


class UserProfile (models.Model):

	MODALIDADE_CHOICES = (
	('GRA', u'Estudante de Graduacao'),
	('PGR', u'Estudante de Pos-Graduacao'),
	('PRO', u'Profissional')
	,)

	minicursos = models.ManyToManyField(Minicurso)
	name = models.CharField(max_length=100)
	instituicao = models.CharField(max_length=200)
	cpf = models.CharField(max_length=11)
	#validacao de cpf usando a lib localflavors no forms.py
	phone = models.CharField(max_length=11)
	#a validacao do telefone e feita pelo localflavors no forms.py
	password = models.CharField(max_length=16)
	#o password e setado como um campo de password no forms.py e nao aqui
	email = models.EmailField(max_length=254)
	comprovante = models.ImageField(upload_to='comprovantes/', default=False)

	modalidade = models.CharField(
		max_length=3,
		choices=MODALIDADE_CHOICES,
		default=False,
	)

	def __str__(self):
		return self.name

class Article (models.Model):
	user = models.ForeignKey(UserProfile)
	title = models.CharField(max_length=100)
	cpf = models.CharField(max_length=11)
	document = models.FileField(upload_to='articles/', default=False)
