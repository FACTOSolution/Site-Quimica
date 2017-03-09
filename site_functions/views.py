from django.shortcuts import render, get_object_or_404
from .forms import *
from .models import UserProfile
from django.shortcuts import redirect


def home(request):
	return render(request, 'site_functions/home.html', {})


def register(request):
	if request.method == "POST":
		new_user = UserForm(request.POST)
		if new_user.is_valid():
			new_user.save()
			return redirect(home)
	else:
		new_user = UserForm(request.POST)
	return render(request, 'site_functions/register.html', {'form': new_user})

def user_login(request):
	if request.method == "POST":
		user = get_object_or_404(UserProfile, email=request.POST.get('email', False))
		if user.password == request.POST.get('psw', False):
			print('something')
		else:
			pass
		return redirect(home)
	else:
		#users = get_object_or_404(UserProfile, email=request.POST.get('email', False))
		#return render(request, 'site_functions/login.html', {'users' : users})
		return render(request, 'site_functions/login.html')


def user_detail(request, pk):
	user = get_object_or_404(UserProfile, pk=pk)
	return render(request, 'site_functions/user_details.html', {'user': user})


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