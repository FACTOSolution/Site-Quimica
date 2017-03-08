from django.shortcuts import render
from .forms import UserForm
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