import urllib
import urllib2
import json
import requests
import hashlib

from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

HOST_URL = "http://127.0.0.1:8081/"


def index(request):
    username = request.session.get('username', None)
    info = request.session
    if not username:
        c = RequestContext(request, {'login': False, 'index': True})
    else:
        c = RequestContext(request, {'login': True, 'info': info, 'index': True})
    return render_to_response('index.html', c)


def signup(request):
    email = request.POST['email']
    password = request.POST['password']
    confirm_password = request.POST['confirm_password']
    username = request.POST['username']
    bio = request.POST['bio']
    signup_status = sendsignuprequest(email, password, confirm_password, username, bio)
    if "up" in signup_status['msg']:
        login_status = sendsigninrequest(username, password)
        print login_status
        if True:
            request.session['username'] = username
            user = json.dumps(login_status['user'])
            user['password'] = hashlib.md5(user['password']).hexdigest()
            request.session['user'] = user
            request.session['friendship'] = json.dumps(login_status['friendship'])
           # print request.session['friendship']
            request.session['history'] = json.dumps(login_status['history'])
            response = {'type': True}
        else:
            response = {'type': False, 'title': "Error",
                        'message': "Auto login failed. Please login yourself."}
    else:
        response = {'type': False, 'title': "Error",
                    'message': signup_status['msg']}
    return HttpResponse(json.dumps(response))


def sendsignuprequest(email, password, confirm_password,  username, bio):
    data = {'email': email, 'password': password, 'confirm_password': confirm_password, 'username': username, 'bio': bio}
    response_json = post(HOST_URL + "signup", data)
    response = json.loads(response_json)
    return response


def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        login_status = sendsigninrequest(username, password)
        if 'success' in login_status['msg']:
            request.session['username'] = username
            user = login_status['user']
            print user['password']
            user['password'] = str(hashlib.md5(user['password']).hexdigest())
            request.session['user'] = json.dumps(user)
            request.session['friendship'] = json.dumps(login_status['friendship'])
            request.session['history'] = json.dumps(login_status['history'])
            #print request.session['history']
            response = {'type': True}
        else:
            response = {'type': False, 'title': "Error",
                        'message': "Your email and password does not match in our system."}
        return HttpResponse(json.dumps(response))
    else:
        if request.method == "GET":
            if 'action' in request.GET:
                action = request.GET['action']
                if action == 'logout':
                    try:
                        del request.session['username']
                        del request.session['email']
                        del request.session['token']
                        del request.session['username']
                    except KeyError:
                        pass
                    return HttpResponse("You're logged out.")


def sendsigninrequest(username, password):
    data = {'username': username, 'password': password}
    response_json = post(HOST_URL + "login", data)
    response = json.loads(response_json)
    return response


def imagesearch(request):
    photo = request.FILES['file']
    addtext = request.POST['additional']
    photoname = 'static/uploads/' + photo.name
    with open(photoname, 'wb+') as destination:
        for chunk in photo.chunks():
            destination.write(chunk)
    files = [('file', (photoname, open(photoname, 'rb'), 'image/' + photo.name.split('.')[1])),
             ('additional', addtext)]
    response_json = requests.post(HOST_URL + 'imagesearch', files=files)
    #print response_json.json()
    return HttpResponse(json.dumps(response_json.json()))


def searchhistory(request):
    base = request.GET['base']
    #print base
    response_json = get(HOST_URL + "history" + "?base=" + base)
    #print response_json
    return HttpResponse(response_json)


def post(url, data):
    req = urllib2.Request(url)
    data = urllib.urlencode(data)
    opener = urllib2.build_opener()
    response = opener.open(req, data)
    return response.read()


def get(url):
    #print url
    req = urllib2.Request(url)
    opener = urllib2.build_opener()
    response = opener.open(req)
    return response.read()
