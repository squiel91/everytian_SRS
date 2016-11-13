from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User, Word, Text, Knowledge
from random import randint
import pdb
import sys
from collections import defaultdict

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
			# pdb.set_trace()
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
		"tweet": "".join(resource.text),
		"word_definitions":resource.definitions_to_json(),
		"translation": resource.translation,
		"audio": resource.audio,
	}

punctuation = u'…！？／（）、，。：「」…『』！？《》“”；’ ‘【】·〔〕.,?!-[]'

def select_next(user):
	actual = None
	max_known_words = 0
	best_sentence = None
	for text in Text.objects.all():
		known_words = 0
		unknown_words = 0
		undefined = 0
		actual = text
		for word in actual.text:
			if word not in punctuation:
				try:
					# pdb.set_trace()
					knowledge = Knowledge.objects.get(user=user, word=word)
					if knowledge.known:
						known_words += 1
					else:
						unknown_words += 1
				except Knowledge.DoesNotExist:
					undefined += 1
		# if text.audio ==333219:
		# 	pdb.set_trace()
		if max_known_words <= known_words and unknown_words + undefined <= 2 and text not in user.resource_history:
			max_known_words = known_words
			best_sentence = text
	
	# print('Goodbye, cruel world!', file=sys.stderr)
	print("known words: {}".format(known_words))
	print("unknown words: {}".format(unknown_words))
	print("undefined: {}".format(undefined))
	# position = randint(1, Text.objects.count()) - 1
	# return Text.objects.all()[position]
	return best_sentence

def practice(request):
	# pdb.set_trace()
	if not request.session.get('email'):
		return redirect('login')
	user = User.objects.get(pk=request.session['email'])

	feedback = defaultdict(list)

	if request.method == "POST":
		# pdb.set_trace()
		resource = Text.objects.get(pk=request.POST["resource_id"])
		all_words = set(resource.text)
		unknown_words = set(request.POST.getlist("unknown"))
		# pdb.set_trace()
		for word_str in all_words:
			try:
				word = Word.objects.get(pk=word_str)
				known = word_str not in unknown_words
				try:
					kng = Knowledge.objects.get(word=word, user=user)
					word_feedback = kng.update_status(known)
					feedback[word_feedback].append(word_str)
				except Knowledge.DoesNotExist:
					Knowledge.objects.create(word=word, user=user, known=known)
					if known:
						feedback["discov_known"].append(word_str)
					else:
						feedback["discov_unknown"].append(word_str)
			except Word.DoesNotExist:
				pass
				
		user.resource_history.append(resource)
		if request.POST.get("favorite") == "on":
			user.favorite_resources.append(resource)
		user.save()
		print(feedback)

	text = select_next(user)
	view_dict = get_view_dict(text)
	view_dict["learned"] = feedback["learned"]
	view_dict["forgotten"] = feedback["forgotten"]
	view_dict["discov_known"] = feedback["discov_known"]
	view_dict["discov_unknown"] = feedback["discov_unknown"]

	return render(request, 'practice.html', view_dict)


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