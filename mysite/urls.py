from django.conf.urls import patterns, include, url
from django.contrib import admin

from views import hello, index, getPhotos, getSinglePhoto, postComment, postRating, searchPosition, recommendation, \
    signup, getRecommendationPhotos, getCluster, cluster, recPlace, getRecPlace
from views import login

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', index),
    url(r'^hello$', hello),
    url(r'^login$', login),
    url(r'^getPhotos', getPhotos),
    url(r'^getSinglePhoto', getSinglePhoto),
    url(r'^postComment', postComment),
    url(r'^postRating', postRating),
    url(r'^searchPosition', searchPosition),
    url(r'^recommendation', recommendation),
    url(r'^getRecommendationPhotos', getRecommendationPhotos),
    url(r'^signup', signup),
    url(r'^cluster', cluster),
    url(r'^getCluster', getCluster),
    url(r'^place', recPlace),
    url(r'^getRecPlace', getRecPlace)

)
