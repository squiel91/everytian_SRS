from django.shortcuts import render, redirect
from ..models import User

def favorites(request):
	if not request.session.get('email'):
		return redirect('login')
	user = User.objects.get(pk=request.session['email'])
	# pdb.set_trace()
	return render(request, 'favorites.html', 
		{"favorites": list(reversed(["".join(fav.text) for fav in user.favorite_resources]))})
