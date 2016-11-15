from django.shortcuts import redirect

def logout(request):
	del request.session['email']
	return redirect('index')