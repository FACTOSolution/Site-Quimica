# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, HttpResponse, HttpResponseRedirect
from .forms import *
from .models import *
from django.shortcuts import redirect
from django.core.mail import EmailMessage, BadHeaderError
from rolepermissions.roles import assign_role
from rolepermissions.checkers import has_permission
from rolepermissions.permissions import grant_permission, revoke_permission


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
			assign_role(user, 'admin')
			#send_email('Confirmação de inscrição',,user.email) Aqui tem que preencher com corpo do email
			return redirect(home)
	else:
		new_user = UserForm()
	return render(request, 'site_functions/register.html', {'form': new_user, 'log':request.session})

def admin_register(request):
	#testado e funcionando
	actual_user = get_object_or_404(UserProfile, id = request.session['member_id'])
	if request.method == "POST":
		new_admin = AdminForm(request.POST)
		if new_admin.is_valid() and has_permission(actual_user, 'add_new_admins'):
			user = new_admin.save()
			assign_role(user, 'admin')
			return redirect(home)
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
			if user.password == request.POST.get('psw', False):
				request.session['is_logged'] = True
				request.session['member_id'] = user.id
				if has_permission(user, 'add_new_admins'):
					print("test")
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
		articles = Article.objects.all().filter(user=user.id)
		return render(request, 'site_functions/user_details.html', {'user': user,'articles':articles, 'log':request.session})
	else:
		user = get_object_or_404(UserProfile, id = request.session['member_id'])
		if has_permission(user,'retrieve_any_student'):
			user_retrieve = get_object_or_404(UserProfile, id=user_id)
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

def mark_payment(request, user_id):
	user = get_object_or_404(UserProfile, id=request.session['member_id'])
	if has_permission(user, 'mark_payment'):
		user_p = get_object_or_404(UserProfile, id=user_id)
		user_p.had_paid = True
		user_p.save()
		#send_email('Confirmação de pagamento',,user_p.email) Aqui tem que preencher com corpo do email
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
				#send_email('Avaliação do artigo - Quimica',article_form.cleaned_data['revision'],
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
			return redirect(home)
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

def edit_short_course(request, short_course_id):
	if request.method == 'POST':
		user = get_object_or_404(UserProfile, id = request.session['member_id'])
		if has_permission(user, 'edit_short_course'):
			form = ShortCourseForm(request.POST)
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
			form = ShortCourseForm()
			return render(request, 'site_functions/edit_short_course.html',
			{'short_course':short_course, 'log':request.session, 'user':user, 'form':form})

def upload_receipt(request):
	if request.method == 'POST':
		receipt = ReceiptForm(request.POST, request.FILES)
		if receipt.is_valid():
			user = get_object_or_404(UserProfile, pk=request.POST['user_id'])
			user.comprovante = receipt.cleaned_data['image_file']
			user.save()
			return redirect(home)
	else:
		receipt = ReceiptForm()
	return render(request, 'site_functions/upload_receipt.html', {'form': receipt})

def upload_article(request):
	#testado e funcionando
	if request.method == 'POST':
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
