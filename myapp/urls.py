from django.contrib import admin
from django.urls import path
from . import views





urlpatterns = [

     path('',views.home,name='home' ),
     path('my/',views.myself,name='myself'),
      path('upload/',views.imageupload.as_view(),name='imageupload'),
      path('login/',views.loginapi.as_view(),name='loginapi'),
      path('search/',views.search, name='search'),
     
      path('unlike/',views.unlike_post,name='unlike'),
       path('like/',views.like_post,name='like'),
       path('profile/',views.profile,name='profile'),
       path('postdata/',views.postdata,name='postdata'),


]


