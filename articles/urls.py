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
    path('journal/<int:year>/<slug:journal_slug>/', views.journal, name='journal'),
    path('journal/<int:year>/<slug:journal_slug>/<slug:article_slug>/', views.journal, name='journal_article'),
    path('ajax/journals/<int:year>', views.ajax_journals, name='ajax_journals'),
    path('ajax/check-year/<int:year>', views.ajax_check_year, name='ajax_check_year'),
    path('ajax/<str:category>/<int:article_id>/<int:start>', views.ajax_load_category, name='ajax_load_category'),
    path('ajax/articles-count/<str:category>', views.ajax_articles_count, name='ajax_articles_count'),
    path('api/articles/', views.api_articles),
    path('api/tags/', views.api_tags),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
handler404 = "articles.views.page_not_found"