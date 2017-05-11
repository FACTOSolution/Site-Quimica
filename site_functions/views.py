# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, HttpResponse, HttpResponseRedirect
from .forms import *
from .models import *
from django.shortcuts import redirect
from django.core.mail import EmailMessage, BadHeaderError
from rolepermissions.roles import assign_role
from rolepermissions.checkers import has_permission
from rolepermissions.permissions import grant_permission, revoke_permission
import os
from django.conf import settings
from django.contrib.auth import hashers as hs
from django.utils.crypto import get_random_string


def home(request):
	#testado e funcionando
	return render(request, 'site_functions/home.html', {'log':request.session})

def administration(request):
	#testado e funcionando
	return render(request, 'site_functions/administration.html', {'log':request.session})

def register(request):
	#testado e funcionando
	if request.method == "POST":
		new_user = UserForm(request.POST)
		if new_user.is_valid():
			user = new_user.save()
			user.password = hs.make_password(request.POST.get('password', False))
			user.confirmation_code = get_random_string(length=16)
			user.save()
			assign_role(user, 'student')
			msg = 'http://localhost:8000/confirm/' + str(user.confirmation_code) + "/" + str(user.id)
			#send_email('Confirmação de inscrição',msg,user.email) Aqui tem que preencher com corpo do email
			return redirect(home)
	else:
		new_user = UserForm()
	return render(request, 'site_functions/register.html', {'form': new_user, 'log':request.session})

def confirm(request, confirmation_code, user_id):
	try:
		user = get_object_or_404(UserProfile, id=user_id)
		if user.confirmation_code == confirmation_code:
			user.is_active = True;
			user.save()
			return redirect(home)
		else:
			return HttpResponse('Codigo de confirmação inválido')
	except:
		return redirect(home)

def admin_register(request):
	#testado e funcionando
	actual_user = get_object_or_404(UserProfile, id = request.session['member_id'])
	if request.method == "POST":
		new_admin = AdminForm(request.POST)
		if new_admin.is_valid() and has_permission(actual_user, 'add_new_admins'):
			user = new_admin.save()
			user.password = hs.make_password(request.POST.get('password', False))
			user.save()
			assign_role(user, 'admin')
			return redirect(administration)
	else:
		new_admin = AdminForm()
	return render(request, 'site_functions/register.html', {'form': new_admin, 'log':request.session})

def user_login(request):
	#testado e funcionando
	if request.method == "POST":
		try:
			user = UserProfile.objects.get(email=request.POST.get('email', False))
		except UserProfile.DoesNotExist:
			return render(request, 'site_functions/login.html', {'message': 'Usuário não cadastrado.'})
		else:
			if hs.check_password(request.POST.get('psw', False), user.password):
				request.session['is_logged'] = True
				request.session['member_id'] = user.id
				if has_permission(user, 'add_new_admins'):
					request.session['is_admin'] = True
				return redirect(home)
			else:
				return render(request, 'site_functions/login.html', {'message': 'Senha incorreta. Tente novamente.'})
	return render(request, 'site_functions/login.html', {'message': 'Entre com seu email e senha.'})

def user_logout(request):
	#testado e funcionando
	try:
		del request.session['member_id']
	except KeyError:
		pass
	try:
		del request.session['is_logged']
	except KeyError:
		pass
	try:
		del request.session['is_admin']
	except KeyError:
		pass
	return redirect(home)

def user_detail(request, user_id):
	#testado e funcionando
	if int(user_id) == int(request.session['member_id']):
		user = get_object_or_404(UserProfile, id = request.session['member_id'])
		print(user.comprovante)
		articles = Article.objects.all().filter(user=user.id)
		form = ReceiptForm()
		return render(request, 'site_functions/user_details.html', {'user': user,'articles':articles, 'log':request.session, 'form': form})
	else:
		user = get_object_or_404(UserProfile, id = request.session['member_id'])
		if has_permission(user,'retrieve_any_student'):
			user_retrieve = get_object_or_404(UserProfile, id=user_id)
			print(user_retrieve.comprovante)
			articles_retrieve = Article.objects.all().filter(user=user_retrieve.id)
			return render(request, 'site_functions/user_details.html', {'user': user_retrieve,
					'articles':articles_retrieve, 'log':request.session})

def list_students(request):
	#testado e funcionando
	user = get_object_or_404(UserProfile, id=request.session['member_id'])
	if has_permission(user, 'list_all_students'):
		Users = UserProfile.objects.filter(groups__name='student')
		return render(request, 'site_functions/list_all_users.html', {'users': Users,
					'log': request.session})
	else:
		return HttpResponse("Nao é Admin")

def list_short_courses(request):
	user = get_object_or_404(UserProfile, id=request.session['member_id'])
	if has_permission(user, 'edit_short_course'):
		scs = Minicurso.objects.all()
		return render(request, 'site_functions/sc_editions.html', {'scs': scs,
					'log': request.session})
	else:
		return HttpResponse("Nao é Admin")

def list_talks(request):
	user = get_object_or_404(UserProfile, id=request.session['member_id'])
	if has_permission(user, 'edit_short_course'):
		talks = Talk.objects.all()
		return render(request, 'site_functions/talk_editions.html', {'talks': talks,
					'log': request.session})
	else:
		return HttpResponse("Nao é Admin")

def mark_payment(request, user_id):
	user = get_object_or_404(UserProfile, id=request.session['member_id'])
	if has_permission(user, 'mark_payment'):
		user_p = get_object_or_404(UserProfile, id=user_id)
		user_p.had_paid = True
		user_p.save()
		msg = "Prezado (a) nome da pessoa \n Informamos a confirmação do pagamento na Jornada de Química. Aproveite o evento e agradecemos a participação \n. A Comissão Organizadora"
		#send_email('Confirmação de pagamento',msg,user_p.email)
		return redirect(home)

def accept_article(request, user_id, article_id):
	user = get_object_or_404(UserProfile, id=request.session['member_id'])
	if request.method == 'POST':
		if has_permission(user, 'revision_article'):
			article_form = ArticleAnalisyForm(request.POST)
			if article_form.is_valid():
				user_p = get_object_or_404(UserProfile, id=user_id)
				article_p = get_object_or_404(Article, id=article_id)
				article_p.accepted = article_form.cleaned_data['accepted']
				article_p.save()
				if (article_form.cleaned_data['accepted'] == 1):
					msg = "Prezado (a) " + str(user.name) + "\n A Comissão Organizadora da Jornada de Química informa que o trabalho " + str(article_p.title) + " foi aceito. Agradecemos a participação"
				elif(article_form.cleaned_data['accepted'] == 0):
					msg = "Prezado (a) " + str(user.name) + "\n A Comissão Organizadora da Jornada de Química, informa que o trabalho "+ str(article_p.title) + " não esteve dentro dos parâmetros requeridos pelo evento, por isso não foi aceito. Embora, agradecemos a participação"
				#send_email('Avaliação do artigo - Quimica',msg,
						# user_p.email)
				return redirect(administration)
		else:
			return redirect(home)
	else:
		article_form = article_form = ArticleAnalisyForm()
		return render(request, 'site_functions/article_revision.html', {'form': article_form,
					'log': request.session})


def register_short_course(request):
	if request.method == 'POST':
		new_short_course = ShortCourseForm(request.POST)
		if new_short_course.is_valid():
			new_short_course.save()
			return redirect(list_short_courses)
	else:
		user = UserProfile.objects.get(pk=request.session['member_id'])
		if has_permission(user, 'create_short_course'):
			new_short_course = ShortCourseForm()
			return render(request, 'site_functions/register.html', {'form': new_short_course, 'log':request.session})
		else:
			return redirect(home)

def short_course_detail(request, short_course_id):
	short_course = get_object_or_404(Minicurso, id = short_course_id)
	user = get_object_or_404(UserProfile, id = request.session['member_id'])
	return render(request, 'site_functions/short_course_details.html', {'short_course':short_course,
			'log':request.session, 'user':user})

def talk_detail(request, talk_id):
	talk = get_object_or_404(Talk, id = talk_id)
	print(talk.talk_name)
	user = get_object_or_404(UserProfile, id = request.session['member_id'])
	return render(request, 'site_functions/talk_details.html', {'talk':talk,
			'log':request.session, 'user':user})

def edit_short_course(request, short_course_id):
	sc_form = get_object_or_404(Minicurso, id=short_course_id)
	if request.method == 'POST':
		user = get_object_or_404(UserProfile, id = request.session['member_id'])
		if has_permission(user, 'edit_short_course'):
			form = ShortCourseForm(request.POST, instance=sc_form)
			short_course = get_object_or_404(Minicurso, id = short_course_id)
			if form.is_valid():
				short_course.name = form.cleaned_data['name']
				short_course.description = form.cleaned_data['description']
				short_course.professor = form.cleaned_data['professor']
				short_course.begin = form.cleaned_data['begin']
				short_course.duration = form.cleaned_data['duration']
				short_course.save()
				return redirect(short_course_detail, short_course_id=short_course_id)
	else:
		user = get_object_or_404(UserProfile, id = request.session['member_id'])
		if has_permission(user, 'edit_short_course'):
			short_course = get_object_or_404(Minicurso, id = short_course_id)
			form = ShortCourseForm(instance=sc_form)
			return render(request, 'site_functions/edit_short_course.html',
			{'short_course':short_course, 'log':request.session, 'user':user, 'form':form})

def edit_talk(request, talk_id):
	talk_form = get_object_or_404(Talk, id=talk_id)
	if request.method == 'POST':
		user = get_object_or_404(UserProfile, id = request.session['member_id'])
		if has_permission(user, 'edit_short_course'):
			form = TalkRegisterForm(request.POST, request.FILES, instance=talk_form)
			talk = get_object_or_404(Minicurso, id = talk_id)
			if form.is_valid():
				talk.talk_name = form.cleaned_data['talk_name']
				talk.talk_description = form.cleaned_data['talk_description']
				talk.talk_speaker = form.cleaned_data['talk_speaker']
				talk.talk_begin = form.cleaned_data['talk_begin']
				talk.talk_local = form.cleaned_data['talk_local']
				talk.talk_speaker_lattes = form.cleaned_data['talk_speaker_lattes']
				talk.talk_speaker_photo = form.cleaned_data['talk_speaker_photo']
				talk.save()
				print(talk.talk_name)
				return redirect(talk_detail, talk_id=talk_id)
	else:
		user = get_object_or_404(UserProfile, id = request.session['member_id'])
		if has_permission(user, 'edit_short_course'):
			talk = get_object_or_404(Talk, id = talk_id)
			form = TalkRegisterForm(instance=talk_form)
			return render(request, 'site_functions/edit_talk.html',
			{'talk':talk, 'log':request.session, 'user':user, 'form':form})

def register_talk(request):
	if request.method == 'POST':
		new_talk_form = TalkRegisterForm(request.POST, request.FILES)
		if new_talk_form.is_valid():
			new_talk_form.save()
			return redirect(list_talks)
	else:
		user = UserProfile.objects.get(pk=request.session['member_id'])
		if has_permission(user, 'create_short_course'):
			new_talk_form = TalkRegisterForm()
			return render(request, 'site_functions/register.html', {'form': new_talk_form, 'log':request.session})
		else:
			return redirect(home)

def upload_receipt(request, user_id):
	if request.method == 'POST':
		if int(user_id) == int(request.session['member_id']):
			receipt = ReceiptForm(request.POST, request.FILES)
			if receipt.is_valid():
				user = get_object_or_404(UserProfile, pk=user_id)
				user.comprovante = receipt.cleaned_data['image_file']
				user.save()
				return redirect(user_detail, user_id)
	else:
		receipt = ReceiptForm()
	return render(request, 'site_functions/upload_receipt.html', {'form': receipt})

def upload_article(request, user_id):
	#testado e funcionando
	if request.method == 'POST':
		if int(user_id) == int(request.session['member_id']):
			article_form = ArticleForm(request.POST, request.FILES)
			if article_form.is_valid():
				Art = Article()
				Art.user = get_object_or_404(UserProfile, id = request.session['member_id'])
				Art.title = request.POST['title']
				Art.document = request.FILES['document']
				Art.save()
				return redirect(user_detail,Art.user.id)
	else:
		article_form = ArticleForm()
	return	render(request, 'site_functions/upload_article.html', {'form': article_form, 'log': request.session})

def send_email(subject, message, to_email):
	if subject and message and to_email:
		try:
			email = EmailMessage(subject, message, to=[to_email])
			email.send()
		except BadHeaderError:
			return HttpResponse('Header invalido')
		return
	else:
		return HttpResponse("Tenha certeza que todos os parametros sao validos")

def download(request, path):
	file_path = os.path.join(settings.MEDIA_ROOT, path)
	if os.path.exists(file_path):
		with open(file_path, 'rb') as fh:
			response = HttpResponse(fh.read(), content_type='application/pdf')
			response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
			return response
	else:
		raise Http404
