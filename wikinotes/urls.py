from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

# Wikinotes stuff
urlpatterns += patterns('wikinotes.views',
	(r'^user/(?P<username>\w+)/*$', 'users.profile'),
	(r'^(?P<department>\w{4})_(?P<number>\d{3})/*$', 'courses.overview'),
	(r'^(?P<department>\w{4})_(?P<number>\d{3})/create/(?P<page_type>\w+)/*$', 'pages.create'),
	(r'^(?P<department>\w{4})/*$', 'departments.overview'),
	(r'^watch/*$', 'courses.watch'),
)