from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from snippets import views


urlpatterns = [
    url(r'^snippets/$', views.SnippetList.as_view()),
    url(r'^snippets/(?P<pk>\d+)/$', views.SnippetDetail.as_view()),
    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>\d+)/$', views.UserDetail.as_view())
]
urlpatterns = format_suffix_patterns(urlpatterns)
