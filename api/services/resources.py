from django.http import JsonResponse, HttpResponse
from ..models import Text
from random import randint

import pdb


def resources(request, id):
	# pdb.set_trace()
	if request.method == "GET":
		resource = None
		if id:
			resource = Text.objects.get(pk=id)
		else:
			position = randint(1, Text.objects.count()) - 1
			resource = Text.objects.all()[position]
		return JsonResponse(resource.serialize())
	if request.method == "POST":
		if id:
			resource = Text.objects.get(pk=id)
			resource.text = request.POST.getlist("text[]")
			resource.translation = request.POST["translation"]
			resource.save()
			return JsonResponse(resource.serialize())
		else:
			HttpResponse("A new resource will be created")
