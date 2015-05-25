from django.conf.urls import patterns, include, url
from django.contrib import admin

from views import *

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', index),
    url(r'^signin', signin),
    url(r'^imagesearch', imagesearch),
    url(r'^searchhistory', searchhistory),
    url(r'^signup', signup),

)
