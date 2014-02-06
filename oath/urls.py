from django.conf.urls import patterns, include, url
from django.contrib.auth.forms import UserCreationForm

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'lab2.views.index'),
    url(r'^profile/(?P<username>(.*))/$','lab2.views.profile'),
    url(r'^login/', 'django.contrib.auth.views.login'),
    url(r'^logout/', 'lab2.views.logout_view'),
    url(r'^register/', 'lab2.views.register'),
    url(r'^oauth/redirect/$', 'lab2.views.handle_oauth'),
    url(r'^oauth/start/$', 'lab2.views.link_oauth'),
    # Examples:
    # url(r'^$', 'lab2.views.home', name='home'),
    # url(r'^oath/', include('oath.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:ls

    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
