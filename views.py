from django.shortcuts import render, redirect, get_object_or_404
from .forms import *

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
