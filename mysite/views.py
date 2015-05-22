import urllib
import urllib2
import json

from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

HOST_URL = "http://127.0.0.1:8081/"


def hello(request):
    return HttpResponse("Hello world")


def index(request):
    email = request.session.get('email', None)
    info = request.session
    if not email:
        c = RequestContext(request, {'login': False, 'index': True})
    else:
        c = RequestContext(request, {'login': True, 'info': info, 'index': True})
    return render_to_response('index.html', c)


def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        login_status = sendLoginRequest(email, password)
        if 'token' in login_status:
            request.session['userId'] = login_status['userId']
            request.session['email'] = login_status['email']
            request.session['token'] = login_status['token']
            request.session['nickName'] = login_status['nickName']
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
                        del request.session['userId']
                        del request.session['email']
                        del request.session['token']
                        del request.session['nickName']
                    except KeyError:
                        pass
                    return HttpResponse("You're logged out.")


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


def sendLoginRequest(email, password):
    data = {'email': email, 'password': password}
    response_json = post(HOST_URL + "signin", data)
    response = json.loads(response_json)
    return response


def sendSignupRequest(email, password, nickname):
    data = {'email': email, 'password': password, 'nickname': nickname}
    response = post(HOST_URL + "signup", data)
    return response


def postComment(request):
    email = request.session.get('email', None)
    if not email:
        response = {'success': False, 'error': "You should log in to make a comment."}
        return HttpResponse(json.dumps(response))
    else:
        photoId = request.POST['photoId']
        text = request.POST['text']
        data = {'userId': request.session['userId'], 'photoId': photoId, 'text': text}
        response_json = post(HOST_URL + "CommentPoster", data)
        response = {'success': True, 'response': response_json}
        return HttpResponse(json.dumps(response))


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


def searchPosition(request):
    API_KEY = "&key=AIzaSyDfZSdXj99Sv1qAvCebtB2DjIrubD6aPKo"
    URL = "https://maps.googleapis.com/maps/api/geocode/json?address="
    address = request.GET['address']
    address = address.replace(" ", "+")
    requestUrl = URL + address + API_KEY
    response = get(requestUrl)
    return HttpResponse(response)


def recommendation(request):
    email = request.session.get('email', None)
    info = request.session
    if not email:
        c = RequestContext(request, {'login': False, 'recommendation': True})
    else:
        c = RequestContext(request, {'login': True, 'info': info, 'recommendation': True})
    return render_to_response('recommendation.html', c)


def getRecommendationPhotos(request):
    userId = request.session['userId']
    data = {'userId': userId}
    response_json = post(HOST_URL + "RecommendationGetter", data)
    return HttpResponse(response_json)


def signup(request):
    email = request.POST['email']
    password = request.POST['password']
    nickname = request.POST['nickname']
    signup_status = sendSignupRequest(email, password, nickname)
    if "true" in signup_status:
        login_status = sendLoginRequest(email, password)
        print login_status
        if 'token' in login_status:
            request.session['userId'] = login_status['userId']
            request.session['email'] = login_status['email']
            request.session['token'] = login_status['token']
            request.session['nickName'] = login_status['nickName']
            response = {'type': True}
        else:
            response = {'type': False, 'title': "Error",
                        'message': "Auto login failed. Please login yourself."}
    else:
        response = {'type': False, 'title': "Error",
                    'message': "Existing user in our system."}
    return HttpResponse(json.dumps(response))


def cluster(request):
    email = request.session.get('email', None)
    info = request.session
    if not email:
        c = RequestContext(request, {'login': False, 'cluster': True})
    else:
        c = RequestContext(request, {'login': True, 'info': info, 'cluster': True})
    return render_to_response('cluster.html', c)


def getCluster(request):
    response_json = get(HOST_URL + "ClusterGetter")
    return HttpResponse(response_json)


def recPlace(request):
    email = request.session.get('email', None)
    info = request.session
    if not email:
        c = RequestContext(request, {'login': False, 'place': True})
    else:
        c = RequestContext(request, {'login': True, 'info': info, 'place': True})
    return render_to_response('place.html', c)


def getRecPlace(request):
    userId = request.session['userId']
    data = {'userId': userId}
    response_json = post(HOST_URL + "PlaceRecommendationGetter", data)
    return HttpResponse(response_json)