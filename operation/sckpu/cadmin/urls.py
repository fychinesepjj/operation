from django.conf.urls import patterns, url

urlpatterns = patterns(
    'cadmin.views',
    url(r'^$', 'index', name='index'),
    url(r'^team/$', 'team', name='team'),
    url(r'^about/$', 'about', name='about'),
    url(r'^project/(\d+)/$', 'project_detail', name='project_detail'),
    url(r'^project/$', 'project', name='project'),
    url(r'^contact/$', 'contact', name='contact'),
)
