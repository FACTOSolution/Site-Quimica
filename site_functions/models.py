# -*- coding: utf-8 -*-
from django.db import models
from .validators import validate_article_type
from django.utils import timezone
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser

class Minicurso (models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField(max_length=6048)
	professor = models.CharField(max_length=100)
	begin = models.CharField(max_length=1024)
	duration = models.DurationField()
	short_course_cover = models.ImageField(upload_to='minicursos/', default=False)
	def __str__(self):
		return self.name


class UserProfile (AbstractBaseUser, PermissionsMixin):

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
	certificado = models.FileField(upload_to='certificados/', default=False, validators=[validate_article_type])
	have_article = models.BooleanField(default=False)
	had_paid = models.BooleanField(default=False)
	have_home = models.BooleanField(default=False)
	confirmation_code = models.CharField(max_length=16, default='aiahisguaeh')
	is_active = models.BooleanField(default=False)


	USERNAME_FIELD = 'email'

	modalidade = models.CharField(
		max_length=3,
		choices=MODALIDADE_CHOICES,
		default=False,
	)

	def __str__(self):
		return self.name

class Article (models.Model):
	user = models.ForeignKey(UserProfile,  on_delete=models.CASCADE, default=False, related_name='Article_User')
	title = models.CharField(max_length=100)
	autores = models.TextField(max_length=300, default=False)

	AREA_CHOICES = (
	('QOR', u'Química Orgânica'),
	('QIN', u'Química Inorgânica'),
	('FSQ', u'Fisico-Química'),
	('QAN', u'Química Analítica'),
	('QAM', u'Química Ambiental'),
	('EAQ', u'Educação Aplicada à Química'),
	('ENG', u'Engenharia'),
	('MAT', u'Materiais'),
	('ALM', u'Alimentos'),
	('TCF', u'Tecnologia Farmacêutica')
,)

	area = models.CharField(
		max_length=3,
		choices=AREA_CHOICES,
		default=False,
	)

	accepted = models.BooleanField(default=False)

	document = models.FileField(upload_to='articles/', default=False, validators=[validate_article_type])

	def __str__(self):
		return self.title

class Talk(models.Model):
	talk_name = models.CharField(max_length=256)
	talk_speaker = models.CharField(max_length=256)
	talk_description = models.CharField(max_length=8128)
	talk_begin = models.DateTimeField(default=timezone.now)
	talk_speaker_lattes = models.CharField(max_length=256, default="")
	talk_speaker_photo = models.ImageField(upload_to='palestrantes/', default=False)
	talk_local = models.CharField(max_length=256, default="")
