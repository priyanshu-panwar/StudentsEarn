from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile, Category, Message, EmailID, AssignRequest, Transaction
from django.http import HttpResponse
from .forms import QuestionForm

def aboutus(request):
	cat = Category.objects.all()
	context = {
		'cat' : cat,
	}
	return render(request, 'core/aboutus.html', context)

def home(request):
	x = False
	if (request.user.is_authenticated):
		p = Profile.objects.filter(user=request.user)
		if (len(p) > 0):
			p = p[0]
		e = EmailID.objects.all()
		for x in e:
			if x.user == request.user:
				x = True
				break

	context = {
		"x" : x,
	}
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
			return redirect('update-mobile', pk=user.id)
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
	# object = get_object_or_404(Profile, pk=pk)
	object = Profile.objects.filter(user__id=pk).first()
	from datetime import date
	today = date.today()
	d1 = today.strftime("%d")
	d1 = int(d1)
	if (d1 == 1):
		object.questions_this_month = 0

	saved = False
	if not object.rank:
		saved = True

	if request.method == "POST":
		form = ProfileForm(request.POST, request.FILES)
		form2 = QuestionForm(request.POST)
		if form.is_valid():
			upi = form.cleaned_data['bank_account']
			ifsc = form.cleaned_data['ifsc_code']
			rank = form.cleaned_data['rank']
			mobile_number = form.cleaned_data['mobile_number']
			subject = form.cleaned_data['subject_choice']
			name = form.cleaned_data['account_holder_name']
			if is_valid_queryparam(name):
				object.account_holder_name = name
				object.save()
			bank = form.cleaned_data['bank_account']
			upi = form.cleaned_data['upi']
			if is_valid_queryparam(bank):
				object.bank_account = bank
				object.save()

			if is_valid_queryparam(upi):
				object.upi = upi
				object.save()
			if is_valid_queryparam(ifsc):
				object.ifsc_code = ifsc
				object.save()
			if is_valid_queryparam(rank):
				object.rank=rank
				object.save()
			if is_valid_queryparam(mobile_number):
				object.mobile_number = mobile_number
				object.save()
			if is_valid_queryparam(subject):
				object.subject_choice = subject
				object.save()
			file = form.cleaned_data['result_file']
			print(request.FILES)
			# print(request.POST['result_file'])
			if is_valid_queryparam(file):
				object.result_file = request.FILES['result_file']
				object.save()
			return redirect('profile', pk=pk)
		if form2.is_valid():
			q = form2.cleaned_data['questions_this_month']
			if is_valid_queryparam(q):
				object.questions_this_month += q;
				object.save()

	form = ProfileForm(initial={'bank_account' : object.bank_account,
		'ifsc_code' : object.ifsc_code,
		'subject' : object.subject_choice,
		'mobile_number' : object.mobile_number,
		'rank' : object.rank,
		'result_file' : object.result_file,
		'upi' : object.upi,
		'bank_account' : object.bank_account,
		'account_holder_name': object.account_holder_name,
	})
	form2 = QuestionForm(initial={'questions_this_month': object.questions_this_month,})
	active = object.is_active
	uploaded = False
	print(object.result_file)
	if object.result_file:
		uploaded = True
	messages = Message.objects.filter(user=request.user)
	# messages = messages[::-1]
	messages = messages[0:3]
	m = request.GET.get('mess')
	print("message = ", m)
	helptext = ""
	assigned = False
	if (object.id_alloted is not None):
		assigned = True
	email_id = None
	pass_word = None
	if assigned:
		email_id = object.id_alloted.Email
		pass_word = object.id_alloted.Password
	if is_valid_queryparam(m):
		me = Message()
		me.user = request.user
		me.message = m
		me.save()
		messages = Message.objects.filter(user=request.user)
		messages = messages[::-1]
		messages = messages[0:3]
		helptext = "Your message is received"
	transactions = Transaction.objects.filter(user=object)
	transactions = transactions[::-1]
	transactions = transactions[0:5]

	context = {
		'transactions' : transactions,
		'email_id' : email_id,
		'pass_word' : pass_word,
		'assigned' : assigned,
		'form' : form,
		'saved' : saved,
		'p' : object,
		'uploaded' : uploaded,
		'active' : active,
		'messages' : messages,
		'helptext' : helptext,
		'form2' : form2,
	}
	return render(request, 'core/profile.html', context)

@login_required()
def assign(request):
	p = Profile.objects.filter(user=request.user).first()
	if p.id_alloted:
		return HttpResponse("Sorry, you have been alloted ID already.")
	if not p.is_active:
		return HttpResponse("Sorry, you are not active to send request.")
	a = AssignRequest()
	a.user = request.user
	print("saving a..")
	a.save()

	return render(request, 'core/assigning.html')

@login_required()
def release(request):
	p = Profile.objects.filter(user=request.user)
	if (len(p) > 0):
		p = p[0]
	e = EmailID.objects.filter(Email=p.id_alloted.Email)
	if (len(e) > 0):
		e = e[0]
		e.release = True
		e.save()
	return render(request, 'core/releasing.html')

from .forms import MobileForm
def update_mobile(request, pk):
	# object = get_object_or_404(Profile, pk=pk)
	object = Profile.objects.filter(user__id=pk).first()
	if request.method == "POST":
		form = MobileForm(request.POST)
		if form.is_valid():
			m = form.cleaned_data['mobile_number']
			if is_valid_queryparam(m):
				object.mobile_number = m
				object.save()
				return redirect('profile', pk=object.user.id)
	form = MobileForm()
	context = {
		'form' : form,
	}
	return render(request, 'core/update_mobile.html', context)
