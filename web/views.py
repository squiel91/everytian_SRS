from django.shortcuts import render
from django.http import HttpResponse
from .models import User, Word
from random import randint
import pdb


# Create your views here.
def index(request):
	return render(request, 'index.html')

def resource(request):
	# pdb.set_trace()
	position = randint(1, Word.objects.count()) - 1
	word = Word.objects.all()[position]
	return render(request, 'resource.html', {
		"hanzi": word.hanzi,
		"pinyin": word.pinyin,
		"definitions": word.definitions
	})

# Create your views here.
def list_users(request):
	users = User.objects.all()
	return render(request, 'list_users.html', {"user_emails": [user.email for user in users]})
