from django.conf.urls import patterns, include, url
from operation.core.utils import site
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^grappelli/', include('operation.core.customs.urls')),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^ueditor/', include('DjangoUeditor.urls')),
    url(r'^admin/', include(site.urls))
)

if settings.DEBUG:
    '''
    When settings.MEDIA_URL = '/' should directly use patterns(..) function
    or use <from django.conf.urls.static import static>
    '''
    urlpatterns += patterns(
        '',
        url(r'^%s(?P<path>.*)$' % settings.MEDIA_URL, 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT})
    )
