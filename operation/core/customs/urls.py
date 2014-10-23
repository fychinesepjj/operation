from django.conf.urls import patterns, url
from django.contrib import admin

from operation.core.customs.views import FilteredAutocompleteLookup

admin.autodiscover()
urlpatterns = patterns(
    '',
    url(r'^lookup/autocomplete/$', FilteredAutocompleteLookup.as_view(), name="grp_autocomplete_lookup"),
)
