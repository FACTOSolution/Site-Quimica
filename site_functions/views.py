from django.shortcuts import render, get_object_or_404, HttpResponse
from .forms import *
from .models import UserProfile
from django.shortcuts import redirect


def home(request):
	return render(request, 'site_functions/home.html', {'log':request.session})


def register(request):
	if request.method == "POST":
		new_user = UserForm(request.POST)
		if new_user.is_valid():
			new_user.save()
			return redirect(home)
	else:
		new_user = UserForm()
	return render(request, 'site_functions/register.html', {'form': new_user, 'log':request.session})

def user_login(request):
	if request.method == "POST":
		user = get_object_or_404(UserProfile, email=request.POST.get('email', False))
		if user.password == request.POST.get('psw', False):
			try:
				if request.session['is_logged'] == True:
					return HttpResponse(u"Você já está autenticado.")
			except KeyError:			
				request.session['is_logged'] = True
				request.session['member_id'] = user.id
				print(request.session.items())
				return HttpResponse(u"Você está autenticado.")
		else:
			return HttpResponse(u"Você não está autenticado.")
		return redirect(home)
	return render(request, 'site_functions/login.html')

def user_logout(request):
	try:
		del request.session['member_id']
	except KeyError:
		pass
	try:
		del request.session['is_logged']
	except KeyError:
		pass
	return redirect(home)

def user_detail(request):
	user = get_object_or_404(UserProfile, id = request.session['member_id'])
	return render(request, 'site_functions/user_details.html', {'user': user, 'log':request.session})

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


#dicionário session