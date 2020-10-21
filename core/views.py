from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile

def home(request):
	return render(request, 'core/index.html')


def login(request):
	pass


def logout(request):
	pass


def is_valid_queryparam(param):
	return param != '' and param is not None

from django.core.files.storage import FileSystemStorage
def register(request):
	fname = request.GET.get('fname')
	lname = request.GET.get('lname')
	username = request.GET.get('username')
	email = request.GET.get('email')
	password1 = request.GET.get('password1')
	mobile_number = request.GET.get('mobile')
	rank = request.GET.get('rank')
	file = request.FILES['fileupload'] if 'fileupload' in request.FILES else None
	
	if is_valid_queryparam(username) and is_valid_queryparam(password1):
		user = User.objects.create_user(username=username, email=email, password=password1, first_name=fname, last_name=lname)
		user.save()
		p = Profile.objects.filter(user=user).last()
		p.mobile_number = mobile_number
		p.rank = rank
		fs = FileSystemStorage()
		f = fs.save(file.name, file)
		p.Files = fs.url(f)
		p.save()

		return render(request, 'core/index.html')

	return render(request, 'core/register.html')



def profile(request):
	pass