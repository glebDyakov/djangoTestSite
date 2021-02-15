from django.views.decorators.cache import cache_page
from django.urls import path
from .views import *
urlpatterns=[
    path('test/',test,name='test'),
    # path('',index),
    path('',cache_page(60)(HomeViews.as_view()),name='home'),
    path('register/',register,name='register'),
path('login/',user_login,name='login'),
path('logout/',user_logout,name='logout'),
    # path('category/<int:category_id>/',get_category,name='category'),
path('category/<int:category_id>/',NewsByCategory.as_view(extra_content={
    'title':"какой-то title"
}),name='category'),
    # path('news/<int:news_id>/',view_news,name='view_news'),
    path('news/<int:pk>/',ViewNews.as_view(),name='view_news'),
    # path('news/add-news/',add_news,name='add_news'),
    path('news/add-news/',CreateView.as_view(),name='add_news'),
    path('test',test),
    path('contact',contact),
]