from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'articles'

urlpatterns = [
    path('', views.index, name='index'),
    path('articles/', views.articles, name='articles'),
    path('article/<slug:slug>/', views.article, name='article'),
    path('news/', views.news, name='news'),
    path('new/<slug:slug>/', views.new, name='new'),
    path('authors/', views.authors, name='authors'),
    path('author/<slug:slug>/', views.author, name='author'),
    path('search/', views.search, name='search'),
    path('tags/', views.tags, name='tags'),
    path('tag/<slug:slug>/', views.tag, name='tag'),
    path('journals/', views.journals, name='journals'),
    path('api/articles/', views.api_articles),
    path('api/tags/', views.api_tags),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
handler404 = "articles.views.page_not_found"