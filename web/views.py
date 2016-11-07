from django.shortcuts import render
from django.http import HttpResponse
from .models import User, Word, Text
from random import randint
import pdb


# Create your views here.
def index(request):
	return render(request, 'index.html')

def resource(request):
	# pdb.set_trace()
	position = randint(1, Text.objects.count()) - 1
	text = Text.objects.all()[position]
	return render(request, 'resource.html', {
		"text": text.text,
		"word_definitions": text.definitions_to_json(),
		"translation": text.translation,
	})

# Create your views here.
def list_users(request):
	users = User.objects.all()
	return render(request, 'list_users.html', {"user_emails": [user.email for user in users]})
