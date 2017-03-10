from django.db import models

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
	('GRA', u'Estudante de Graduação'),
	('PGR', u'Estudante de Pós-Graduação'),
	('PRO', u'Profissional')
,)

	minicursos = models.ManyToManyField(Minicurso)
	name = models.CharField(max_length=100)
	instituicao = models.CharField(max_length=200)
	cpf = models.CharField(max_length=11)
	#validação de cpf usando a lib localflavors no forms.py
	phone = models.CharField(max_length=11)
	#a validação do telefone é feita pelo localflavors no forms.py
	password = models.CharField(max_length=16)
	#o password é setado como um campo de password no forms.py e não aqui
	email = models.EmailField(max_length=254, unique=True)
	comprovante = models.ImageField(upload_to='comprovantes/', default=False)
	have_article = models.BooleanField(default=False)
	
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