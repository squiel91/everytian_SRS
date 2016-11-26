from django.shortcuts import render, redirect
from random import randint
from ..models import Text
import pdb

def resources(request):
	if request.method == "GET":
		position = randint(1, Text.objects.count()) - 1
		text = Text.objects.all()[position]
		return render(request, 'resources.html', {"resource_id": str(text.id)})