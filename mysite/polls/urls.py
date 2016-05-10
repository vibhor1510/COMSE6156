from django.conf.urls import patterns, url

from . import views

app_name = 'polls'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^all/$', views.all, name='all'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^signupclick/$', views.signupclick, name='signupclick'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^addQuestion/$', views.addQuestion, name='addQuestion'),
    url(r'^addAnswer/(?P<id>[0-9]+)/$', views.addAnswer, name='addAnswer'),
    url(r'^addCommentRoot/(?P<id>[0-9]+)/$', views.addCommentRoot, name='addCommentRoot'),
    url(r'^posting/(?P<id>[0-9]+)/$', views.posting, name='posting'),
    url(r'^likePost/(?P<id>[0-9]+)/$', views.likePost, name='likePost'),
    url(r'^UnlikePost/(?P<id>[0-9]+)/$', views.UnlikePost, name='UnlikePost'),
    url(r'^votePost/(?P<pid>[0-9]+)/(?P<aid>[0-9]+)/$', views.votePost, name='votePost'),
    url(r'^unvotePost/(?P<pid>[0-9]+)/(?P<aid>[0-9]+)/$', views.unvotePost, name='unvotePost'),
    url(r'^likeComment/(?P<pid>[0-9]+)/(?P<cid>[0-9]+)/$', views.likeComment, name='likeComment'),
    url(r'^UnlikeComment/(?P<pid>[0-9]+)/(?P<cid>[0-9]+)/$', views.UnlikeComment, name='UnlikeComment'),
    url(r'^list/$', views.list, name='list'),    
]



