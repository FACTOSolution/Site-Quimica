from django.db import models
from validators import validate_article_type

class Minicurso (models.Model):
	mini_id = models.IntegerField(unique=True)
	name = models.CharField(max_length=100)
	description = models.TextField(max_length=400)
	professor = models.CharField(max_length=100)
	begin = models.DateTimeField()
	duration = models.DurationField()

	def __str__(self):
		return self.name


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
	email = models.EmailField(max_length=254, unique=True)
	comprovante = models.ImageField(upload_to='comprovantes/', default=False)
	have_article = models.BooleanField(default=False)
	had_paid = models.BooleanField(default=False)

	modalidade = models.CharField(
		max_length=3,
		choices=MODALIDADE_CHOICES,
		default=False,
	)

	def __str__(self):
		return self.name

class Article (models.Model):
	user = models.ForeignKey(UserProfile,  on_delete=models.CASCADE, default=False)
	title = models.CharField(max_length=100)
	document = models.FileField(upload_to='articles/', default=False, validators=[validate_article_type])

	def __str__(self):
		return self.title
