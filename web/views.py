from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User, Word, Text
from random import randint
import pdb


# Create your views here.
def index(request):
	return render(request, 'index.html')

def register(request):
	if request.method == "GET":
		return render(request, 'register.html')
	else:
		email = request.POST.get("email", None)
		name = request.POST.get("name", None)
		password = request.POST.get("password", None)
		retyped_pass = request.POST.get("retyped_pass", None)
		method = request.POST.get("method", None)
		pronunciation = request.POST.get("pronunciation", None)

		User.objects.create(
			email=email,
			name=name,
			password=password,
			simplified=method,
			pronunciation=pronunciation
		)
		request.session['email'] = email
		return redirect('resource')

def login(request):
	if request.method == "GET":
		return render(request, 'login.html')
	else:
		email = request.POST.get("email", None)
		password = request.POST.get("password", None)
		try:
			user = User.objects.get(pk=email)
		except User.DoesNotExist:
			return render(request, 'login.html', { 
				"error": "Email address doesnt exist!" })

		if user.password == password:
			request.session['email'] = email
			return redirect('resource')
		else:
			return render(request, 'login.html', { 
				"error": "Password doesnt match!" })

def logout(request):
	del request.session['email']
	return redirect('index')

def resource(request):
	if not request.session.get('email'):
		return redirect('login')
	user = User.objects.get(pk=request.session['email'])
	position = randint(1, Text.objects.count()) - 1
	text = Text.objects.all()[position]
	return render(request, 'resource.html', {
		"user": user.name,
		"text": text.text,
		"word_definitions": text.definitions_to_json(),
		"translation": text.translation,
		"audio": text.audio,
		
	})

# Create your views here.
def list_users(request):
	users = User.objects.all()
	return render(request, 'list_users.html', {"user_emails": [user.email for user in users]})
