from django.shortcuts import render, redirect

def index(request):
	if request.session.get("email", None):
		return redirect('practice')
	return render(request, 'index.html')