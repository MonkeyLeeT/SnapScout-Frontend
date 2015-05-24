import urllib
import urllib2
import json

from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

HOST_URL = "http://127.0.0.1:8081/"


def index(request):
    username = request.session.get('username', None)
    print username
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
        login_status = sendsigninrequest(email, password)
        if 'token' in login_status:
            request.session['email'] = login_status['email']
            request.session['token'] = login_status['token']
            request.session['username'] = login_status['username']
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
    print response
    return response


def getPhotos(request):
    season = request.GET['season']
    lat1 = request.GET['lat1']
    lat2 = request.GET['lat2']
    lng1 = request.GET['lng1']
    lng2 = request.GET['lng2']
    data = {'season': season, 'lat1': lat1, 'lat2': lat2, "lng1": lng1, "lng2": lng2}
    response_json = post(HOST_URL + "PhotoGetter", data)
    return HttpResponse(response_json)


def getSinglePhoto(request):
    photoId = request.GET['photoId']
    userId = request.session.get('userId', -1)
    data = {'photoId': photoId, 'userId': userId}
    response_json = post(HOST_URL + "SinglePhotoGetter", data)
    return HttpResponse(response_json)


def post(url, data):
    req = urllib2.Request(url)
    data = urllib.urlencode(data)
    opener = urllib2.build_opener()
    response = opener.open(req, data)
    return response.read()


def get(url):
    req = urllib2.Request(url)
    opener = urllib2.build_opener()
    response = opener.open(req)
    return response.read()


def postRating(request):
    email = request.session.get('email', None)
    if not email:
        response = {'success': False, 'error': "You should log in to make a comment."}
        return HttpResponse(json.dumps(response))
    else:
        photoId = request.POST['photoId']
        rating = request.POST['rating']
        data = {'userId': request.session['userId'], 'photoId': photoId, 'rank': rating}
        response_json = post(HOST_URL + "RatingPoster", data)
        response = {'success': True, 'response': response_json}
        return HttpResponse(json.dumps(response))