from django.shortcuts import render
from main.models import *
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest, Http404,JsonResponse
from django.contrib.auth.models import User,Group
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
def home(request):
	return render(request,'homepage/index.html',{})


def signup(request):
	response={}
	if request.method == 'POST':
		firstname = request.POST['firstname']
		lastname = request.POST['lastname']
		username = request.POST['email']
		email = request.POST['email']
		password1 = request.POST['password']
		password2 = request.POST['confirm_password']

		if password1!=password2:
			response['message'] = "Password does not match"
			return render(request,'main/site/signup.djt',response)

		user = User()
		user.first_name = firstname
		user.last_name = lastname
		user.username = username
		user.email = email
		user.set_password(password1)
		try:
			user.save()
			response['message'] = "Successfully Registered"
			p = UserProfile()
			p.user = user
			p.organisation = request.POST['organisation']
			p.address = request.POST['address']
			p.mobile_no = request.POST['mobile_no']
			p.save()
			return render(request,'main/site/login.djt',response)
		except :
			response['message'] = "username already exist"
			return render(request,'main/site/signup.djt',response)
	return render(request,'main/site/signup.djt')

def signin(request):
	response={}
	if request.user.is_authenticated():
	    return HttpResponseRedirect('/')
	if request.method == "POST":
	    username = request.POST['username']
	    password = request.POST['password']
	    user = authenticate(username=username, password=password)
	    if user is not None:
	        login(request, user)
	        return HttpResponseRedirect('/main/dashboard/')
	    else:
	        response['message']='User is not registered / Password Incorrect' 
	return render(request,'main/site/login.djt',response)

def signout(request):
	logout(request)
	return HttpResponseRedirect('/')

@login_required(login_url='/main/signin/')
def uploadpaper(request):
	if request.method == 'POST':
		if request.FILES:
			b = BluePrint()
			b.user = request.user
			b.name = request.POST['name']
			b.desp = request.POST['desp']
			b.blueprint = request.FILES['blueprint']
			b.save()
			return HttpResponseRedirect('/main/dashboard/')
	return render(request,'main/site/uploadprint.djt',{})

@login_required(login_url='/main/signin/')
def dashboard(request):
	blueprints = BluePrint.objects.filter(user=request.user)
	response = {}
	response['blueprints'] = blueprints
	return render(request,'main/site/dashboard.djt',response)

