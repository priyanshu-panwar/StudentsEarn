from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile

def home(request):
	return render(request, 'core/index.html')


def login(request):
	if request.method == 'POST':
		username_ = request.POST['username']
		pass_ = request.POST['password']
		print(username_)
		print(pass_)
		user = authenticate(request, username=username_, password=pass_)
		if user is not None:
			auth_login(request, user)
			return redirect('profile', pk=user.id)
		else:
			return render(request, 'core/index.html', {"unsaved" : "incorrect details."})
	else:
		return render(request, 'core/login.html')


def logout(request):
	auth_logout(request)
	return render(request, 'core/index.html')


def is_valid_queryparam(param):
	return param != '' and param is not None

from django.core.files.storage import FileSystemStorage
from .forms import ProfileForm
def register(request):
	if request.method == "POST":
		fname = request.POST['fname']
		lname = request.POST['lname']
		username = request.POST['username']
		email = request.POST['email']
		password1 = request.POST['password1']
		
		print(lname)
		pf = ProfileForm(request.POST, request.FILES)
		if is_valid_queryparam(username) and is_valid_queryparam(password1):
			user = User.objects.create_user(username=username, email=email, password=password1, first_name=fname, last_name=lname)
			user.save()
			pro = Profile.objects.filter(user=user).last()
			print("user saved")
			auth_login(request, user)
			context = {
				'info' : "Please update your info. Upload you result.",
				'profile' : pro,
			}
			return redirect('profile', pk=user.id)
			# print(request.FILES)
			"""if pf.is_valid():
				p = pf.save(commit=False)
				p.user = user
				p.save()
				print(pf.cleaned_data["result_file"])
				print(pf.cleaned_data["rank"])
				
				# myfile = request.FILES['myfile']
				# fs = FileSystemStorage()
				# filename = fs.save(myfile.name, myfile)
				# uploaded_file_url = fs.url(filename)
				# p.Files = request.FILES['Files']
				print("saved form")
"""
			return render(request, 'core/index.html', {'saved' : True})
	else:
		pf = ProfileForm()
		return render(request, 'core/register.html', {'pf' : pf, })

	return render(request, 'core/register.html', {'pf' : pf,})



def profile(request, pk):
	object = get_object_or_404(Profile, pk=pk)
	saved = False
	if not object.rank:
		saved = True

	if request.method == "POST":
		form = ProfileForm(request.POST, request.FILES)
		if form.is_valid():
			upi = form.cleaned_data['upi']
			rank = form.cleaned_data['rank']
			mobile_number = form.cleaned_data['mobile_number']
			if is_valid_queryparam(upi):
				object.upi = upi
				object.save()
			if is_valid_queryparam(rank):
				object.rank=rank
				object.save()
			if is_valid_queryparam(mobile_number):
				object.mobile_number = mobile_number
				object.save()
			file = form.cleaned_data['result_file']
			if is_valid_queryparam(file):
				object.result_file = file
				object.save()
			return redirect('profile', pk=pk)

	form = ProfileForm(initial={'upi' : object.upi,
		'subject' : object.subject,
		'mobile_number' : object.mobile_number,
		'rank' : object.rank,
	})
	context = {
		'form' : form,
		'saved' : saved,
		'p' : object,
	}
	return render(request, 'core/profile.html', context)