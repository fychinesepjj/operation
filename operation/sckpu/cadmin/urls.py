from django.conf.urls import patterns, url

urlpatterns = patterns(
    'cadmin.views',
    url(r'^$', 'index'),
    url(r'^team/$', 'team'),
    url(r'^about/$', 'about'),
    url(r'^project/$', 'project'),
    url(r'^contact/$', 'contact'),
)
