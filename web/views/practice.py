from django.shortcuts import render, redirect
from django.http import HttpResponse
from ..models import User, Word, Text, Knowledge, EvolutionRecord
from random import randint
import pdb
import sys
from collections import defaultdict

def practice(request):
	# pdb.set_trace()
	if not request.session.get('email'):
		return redirect('login')
	user = User.objects.get(pk=request.session['email'])


	return render(request, 'practice.html', {"user_email": user.email})
