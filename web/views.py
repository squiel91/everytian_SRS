from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User, Word, Text, Knowledge
from random import randint
import pdb


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
		return redirect('practice')

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
			return redirect('practice')
		else:
			return render(request, 'login.html', { 
				"error": "Password doesnt match!" })

def logout(request):
	del request.session['email']
	return redirect('index')

def get_view_dict(resource):
	return {
		"resource_id": resource.id,
		"text": resource.text,
		"word_definitions":resource.definitions_to_json(),
		"translation": resource.translation,
		"audio": resource.audio,
	}

def practice(request):
	if not request.session.get('email'):
		return redirect('login')
	user = User.objects.get(pk=request.session['email'])

	if request.method == "POST":
		# pdb.set_trace()
		resource = Text.objects.get(pk=request.POST["resource_id"])
		all_words = set(resource.text)
		unknown_words = set(request.POST.getlist("unknown"))
		known_words = all_words - unknown_words
		
		for known_word in known_words:
			try:
				word = Word.objects.get(pk=known_word)
				try:
					Knowledge.objects.get(word=known_word, user=user).update(known=True)
				except Knowledge.DoesNotExist:
					Knowledge.objects.create(word=known_word, user=user, known=True)
			except Word.DoesNotExist:
				pass
		for unknown_word in unknown_words:
			try:
				word = Word.objects.get(pk=unknown_word)
				try:
					Knowledge.objects.get(word=unknown_word, user=user).update(known=False)
				except Knowledge.DoesNotExist:
					Knowledge.objects.create(word=unknown_word, user=user, known=False)
			except Word.DoesNotExist:
				pass
				
		user.resource_history.append(resource)
		if request.POST.get("favorite") == "on":
			user.favorite_resources.append(resource)
		user.save()


	position = randint(1, Text.objects.count()) - 1
	text = Text.objects.all()[position]
	return render(request, 'practice.html', get_view_dict(text))


def favorites(request):
	if not request.session.get('email'):
		return redirect('login')
	user = User.objects.get(pk=request.session['email'])
	# pdb.set_trace()
	return render(request, 'favorites.html', 
		{"favorites": ["".join(fav.text) for fav in user.favorite_resources]})

def evolution(request):
	return render(request, 'evolution.html')

def settings(request):
	return render(request, 'settings.html')