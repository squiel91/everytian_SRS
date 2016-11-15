from django.shortcuts import render, redirect
from ..models import User


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