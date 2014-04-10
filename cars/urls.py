from django.conf.urls import patterns, url
from cars  import views

urlpatterns = patterns('',
    url(r'^$', views.CarMarksView.as_view(), name='car-marks-view', ),
    url(r'^search$', views.SearchView.as_view(), name = 'search-view', ),
    #url(r'^(?P<pk>\d+)/$', views.SearchView.as_view(),name='search-view',),

)