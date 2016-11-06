from django.shortcuts import render
from django.http import HttpResponse
from .models import User


# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, 'index.html')

def create_user(request):
    # return HttpResponse('Hello from Python!')
    User.objects.create(email="new@new.com", first_name="New", last_name="New")
    return HttpResponse("Ready!")

# Create your views here.
def list_users(request):
    # return HttpResponse('Hello from Python!')
    users = User.objects.all()
    return render(request, 'list_users.html', {"user_emails": [user.email for user in users]})
