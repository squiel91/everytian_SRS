from django.shortcuts import render, redirect
from ..models import User


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