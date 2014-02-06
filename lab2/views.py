from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.template import RequestContext
from django import forms
import foursquare
from lab2.models import foursquareInfo

def index(request):
    allUsers = User.objects.all()
    curUser = User.objects.filter(username=request.user.username)
    if request.user.is_authenticated():
        output = '<br> You are Logged in as : ' + curUser[0].username
    else :
        output = 'You are Not Currently Logged In'

    output += '<br><br><a href="http://127.0.0.1:8000/login/">Login</a><br>'
    output += '<a href="http://127.0.0.1:8000/logout/">Logout</a><br>'
    output += '<a href="http://127.0.0.1:8000/register/">Sign Up</a><br>'

    output += '<br>All Accounts <br>'
    for u in allUsers  :
        output += '<br><a href="http://127.0.0.1:8000/profile/' + u.username + '"/>' + u.username + '</a>'

    return HttpResponse(output)

def logout_view(request):
    logout(request)
    return HttpResponse("You have been logged out")


def register(request):
    if request.method == 'POST':
         form = UserCreationForm(request.POST)
         if form.is_valid():
             new_user = form.save()
             return HttpResponseRedirect("/login/")
    else:
        form = UserCreationForm()
    c = {'form': form}
    return render_to_response("registration/register.html", c, context_instance=RequestContext(request))

def handle_oauth(request):
    code = request.GET.get('code', None)
    client = newClient()
    access_token = client.oauth.get_token(code)
    client.set_access_token(access_token)
    user = client.users()['user']
    userId = request.user.id
    a = foursquareInfo(user_id=userId, access_token=code, fs_id=user['id'])
    a.save()
    return HttpResponseRedirect("/profile/" + str(userId))


def link_oauth(request):
    client = newClient();
    auth_uri = client.oauth.auth_url()
    return HttpResponseRedirect(auth_uri)

def newClient():
    return foursquare.Foursquare(client_id='TF2MTI1FCUBHOV1EHJUDV42XT0M3QR2KXAUBSAXNIRHTJHIO',
                               client_secret='GAU0OYF2DUJQQ3VWVVB5GMUGAWIIV0L0WD434GHQXEWNKM4R',
                               redirect_uri='ec2-54-202-45-161.us-west-2.compute.amazonaws.com/oath/redirect')

def userClient(userId):
    access = foursquareInfo.objects.filter(user_id=userId)[0].access_token
    return foursquare.Foursquare(access_token=access)


def profile(request, username):
    output = "";
    if request.user.is_authenticated() and request.user.username == username:
        output += "This is your profile Page"



    output += '<br><a href="http://127.0.0.1:8000/Oath/">Link Account to FourSquare</a><br>'

    return HttpResponse("You're looking at the profile of " + username + "<br>" + output  )
