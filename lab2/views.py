from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.template import RequestContext
from django import forms
import foursquare
from lab2.models import foursquareinfo

def index(request):
    allUsers = User.objects.all()
    curUser = User.objects.filter(username=request.user.username)
    if request.user.is_authenticated():
        output = '<br> You are Logged in as : ' + curUser[0].username
    else :
        output = 'You are Not Currently Logged In'

    output += '<br><br><a href="/login/">Login</a><br>'
    output += '<a href="/logout/">Logout</a><br>'
    output += '<a href="/register/">Sign Up</a><br>'

    output += '<br>All Accounts <br>'
    for u in allUsers  :
        output += '<br><a href="/profile/' + u.username + '"/>' + u.username + '</a>'

    return HttpResponse(output)

def logout_view(request):
    logout(request)
    return HttpResponse('You have been logged out! <br> <a href="/">Home Page</a><br>')


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

def newClient():
    return foursquare.Foursquare(client_id='TF2MTI1FCUBHOV1EHJUDV42XT0M3QR2KXAUBSAXNIRHTJHIO',
                               client_secret='GAU0OYF2DUJQQ3VWVVB5GMUGAWIIV0L0WD434GHQXEWNKM4R',
                               redirect_uri='http://ec2-54-202-45-161.us-west-2.compute.amazonaws.com/oauth/redirect')

def handle_oauth(request):
    code = request.GET.get('code', None)
    client = newClient()
    access_token = client.oauth.get_token(code)
    client.set_access_token(access_token)
    user = client.users()['user']
    username = request.user.username
    a = foursquareinfo(username=username, access_token=code, fs_id=user['id'])
    a.save()
    return HttpResponseRedirect("/profile/" + str(username))


def link_oauth(request):
    client = newClient()
    auth_uri = client.oauth.auth_url()
    return HttpResponseRedirect(auth_uri)



def userClient(username):
    access = foursquareinfo.objects.filter(username=username)[0].access_token
    return foursquare.Foursquare(access_token=access)


def profile(request, username):
    output = ""
    a = foursquareinfo.objects.filter(username=username)
    if (not request.user.is_authenticated()) or (request.user.is_authenticated and request.user.username != username):
        if len(a) > 0:
            client = userClient(username)
            checkin = client.users.checkins()['checkins']['items']
            output += "<br> Last Checkout : "
            if len(checkin) > 0:
                x = checkin[0]
                output += '<br>Location: ' + str(x['venue']['name']) +\
                        ' <br>ShoutOut: ' + str(x['shout']) +\
                        ' <br>Total Checkins: ' + str(x['venue']['stats']['checkinsCount'])
        else:
            output += '<br> He has not gone anywhere yet yet'
    else :
        output += "This is your profile Page<br>"
        if (len(a) > 0):
            client = userClient(username)
            checks = client.users.checkins()['checkins']['items']
            body = "Full profile. Code = " + a[0].access_token
            output += '<br>Checkins: <br>'
            for x in checks:
                 output += '<br>Location: ' + str(x['venue']['name']) +\
                        ' <br>ShoutOut: ' + str(x['shout']) +\
                        ' <br>Total Checkins: ' + str(x['venue']['stats']['checkinsCount'])
        else:
            output = 'No account connected. <a href=\"/oauth/start\">Click here to link accounts</a>'

    return HttpResponse("You're looking at the profile of " + username + "<br>" + output + '<br> <a href="/">Home Page</a><br>')
