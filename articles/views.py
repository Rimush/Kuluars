from django.shortcuts import render, get_object_or_404
from .models import Article, Author, Journal
from comments.models import Comment
from comments.forms import CommentForm
from django.utils import timezone
from django.db.models import Q
from django.views.generic import TemplateView, ListView
from taggit.models import Tag
from django.core import serializers
from django.http import JsonResponse
from .serializers import articles_serializer, tags_serializer
from datetime import datetime
import json

CONST_ARTICLES = 4
CONST_NEWS = 9
 
def api_articles(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = articles_serializer(articles, many=True)
        return JsonResponse(serializer.data, safe=False)
 
def api_tags(request):
    if request.method == 'GET':
        tags = Tag.objects.all()
        serializer = tags_serializer(tags, many=True)
        return JsonResponse(serializer.data, safe=False)
 
# последние комментарии
def last_comments():
    comments = Comment.objects.order_by('-created')
    comments = comments[:3]
    
    limit_head = 25
    limit_text = 50
    
    for comment in comments:
        comment.content_short = comment.content
        comment.article.title_short = comment.article.title
        if len(comment.content) > limit_text: 
            comment.content_short = comment.content[:limit_text] + '...'
        if len(comment.article.title) > limit_head: 
            comment.article.title_short = comment.article.title[:limit_head] + '...'
     
    return comments

def random_author():
    author = Author.objects.order_by('?')
    if len(author) == 0:
        return None
    else:
        return author[0]
    
def random_authors():
    authors = Author.objects.order_by('?')
    if len(authors) == 0:
        return None
    else:
        return authors[:4]
    
def more_articles(category, article=None):
    if article == None:
        return None
    else:
        return Article.objects.filter(category=category).filter(~Q(id=article.id)).order_by('-created')

# лучшии статьи за неделю  
def best_week_articles():
    articles = Article.objects.filter(created__range=[timezone.now() - timezone.timedelta(7), timezone.now()]).order_by('views')
    return articles[:3]

# Create your views here.
def index(request):
    articles = Article.objects.filter(category='article').order_by('-created')
    news = Article.objects.filter(category='news').order_by('-created')
    context = {}
    context.update({'articles': articles})
    context.update({'news': news})
    context.update({'best_week_articles': best_week_articles()})
    context.update({'random_author': random_author()})
    context.update({'last_comments': last_comments()})
    
    return render(request, 'page_main__index.html', context)

def articles(request):
    global CONST_ARTICLES
    article = Article.objects.filter(category='article').order_by('-created')
    if len(article) == 0:
        article = None
        author_articles = None
        author_articles_count = None
    else:
        article = article[0]

        if article.author == None:
            author_articles = None
            author_articles_count = None
        else:
            author_articles = Article.objects.filter(author_id=article.author.id, category='article').order_by('-created')
            author_articles_count = len(author_articles)
            author_articles = author_articles [:3]
    
    context = {}
    context.update({'article': article})
    context.update({'author_articles': author_articles})
    context.update({'author_articles_count': author_articles_count})
    context.update({'best_week_articles': best_week_articles()})
    context.update({'random_author': random_author()})
    context.update({'random_authors': random_authors()})
    context.update({'more_articles': more_articles('article', article)[0:CONST_ARTICLES]})
    context.update({'last_comments': last_comments()})
    
    return render(request, 'page_articles__list.html', context)
    
def article(request, slug):
    article = get_object_or_404(Article, slug=slug)
    # считаем просмотры
    article.views = article.views + 1
    article.save()

    # Если автора нет
    if article.author == None: 
        author_articles = None
        author_articles_count = None
    else:
        author_articles = Article.objects.filter(author_id=article.author.id, category='article').order_by('-created')
        author_articles_count = len(author_articles)
        author_articles = author_articles [:3]

    # Статьи ранее
    deep = 3
    earlier = []
    earlier_list = [article]
    while deep != 0:
        deep -= 1
        earlier_tmp = []
        for item in earlier_list:
            if item.earlier != None:
                earlier.append(item.earlier)
                earlier_tmp.append(item.earlier)
        earlier_list = earlier_tmp
    if earlier == []: earlier = [None]
    
    # Список активных комментариев к этой записи  
    comments = article.comments.filter(active=True)  
    new_comment = None  
    if request.method == 'POST':  
        comment_form = CommentForm(data=request.POST)  
        if comment_form.is_valid():  
            new_comment = comment_form.save(commit=False)  
            new_comment.article = article
            #new_comment.ip = request.META.get('REMOTE_ADDR')
            new_comment.save() 
    else:  
        comment_form = CommentForm()  

    context = {}
    context.update({'article': article})
    context.update({'earlier': earlier})
    context.update({'author_articles': author_articles})
    context.update({'author_articles_count': author_articles_count})
    context.update({'comments': comments})
    context.update({'new_comment': new_comment})
    context.update({'comment_form': comment_form})
    context.update({'best_week_articles': best_week_articles()})
    context.update({'random_author': random_author()})
    context.update({'random_authors': random_authors()})
    context.update({'more_articles': more_articles('article', article)[0:CONST_ARTICLES]})
    context.update({'last_comments': last_comments()})
    
    return render(request, 'page_articles__article.html', context)
   
def news(request):
    global CONST_NEWS
    new = Article.objects.filter(category='news').order_by('-created')
    if len(new) == 0:
        new = None
        important = None
        earlier = None
        comments = None
        new_comment = None  
    else:
        new = new[0]
        important = Article.objects.filter(important=True, category='news').filter(~Q(id=new.id)).order_by('-created')[:3]

        # считаем просмотры
        new.views = new.views + 1
        new.save()

        # Статьи ранее
        deep = 3
        earlier = []
        earlier_list = [new]
        while deep != 0:
            deep -= 1
            earlier_tmp = []
            for item in earlier_list:
                if item.earlier != None:
                    earlier.append(item.earlier)
                    earlier_tmp.append(item.earlier)
            earlier_list = earlier_tmp
        if earlier == []: earlier = [None]    
        
        # Список активных комментариев к этой записи  
        comments = new.comments.filter(active=True)  
    
    new_comment = None  
    if request.method == 'POST':  
        comment_form = CommentForm(data=request.POST)  
        if comment_form.is_valid():  
            new_comment = comment_form.save(commit=False)  
            new_comment.article = new
            #new_comment.ip = request.META.get('REMOTE_ADDR')
            new_comment.save() 
    else:  
        comment_form = CommentForm() 

    context = {}
    context.update({'new': new})
    context.update({'earlier': earlier})
    context.update({'important': important})
    context.update({'comments': comments})
    context.update({'new_comment': new_comment})
    context.update({'comment_form': comment_form})
    context.update({'best_week_articles': best_week_articles()})
    context.update({'random_author': random_author()})
    context.update({'more_news': more_articles('news', new)[0:CONST_NEWS]})
    context.update({'last_comments': last_comments()})
    
    return render(request, 'page_news__list.html', context)
   
def new(request, slug):
    global CONST_NEWS
    new = get_object_or_404(Article, slug=slug)
    important = Article.objects.filter(important=True, category='news').filter(~Q(id=new.id)).order_by('-created')[:3]
    
    # считаем просмотры
    new.views = new.views + 1
    new.save()
    
    # Статьи ранее
    deep = 3
    earlier = []
    earlier_list = [new]
    while deep != 0:
        deep -= 1
        earlier_tmp = []
        for item in earlier_list:
            if item.earlier != None:
                earlier.append(item.earlier)
                earlier_tmp.append(item.earlier)
        earlier_list = earlier_tmp
    if earlier == []: earlier = [None]    
    
    # Список активных комментариев к этой записи  
    comments = new.comments.filter(active=True)  
    new_comment = None  
    if request.method == 'POST':  
        comment_form = CommentForm(data=request.POST)  
        if comment_form.is_valid():  
            new_comment = comment_form.save(commit=False)  
            new_comment.article = new
            #new_comment.ip = request.META.get('REMOTE_ADDR')
            new_comment.save() 
    else:  
        comment_form = CommentForm() 

    context = {}
    context.update({'new': new})
    context.update({'earlier': earlier})
    context.update({'important': important})
    context.update({'comments': comments})
    context.update({'new_comment': new_comment})
    context.update({'comment_form': comment_form})
    context.update({'best_week_articles': best_week_articles()})
    context.update({'random_author': random_author()})
    context.update({'more_news': more_articles('news', new)[0:CONST_NEWS]})
    context.update({'last_comments': last_comments()})

    return render(request, 'page_news__new.html', context)
    
def journals(request):
    journals = Journal.objects.filter(year=datetime.now().year).order_by('-index')
    
    if len(journals) == 0:
        journals = None
        journal = None
        articles = None
        article = None
        earlier = None
        comments = None
        new_comment = None
        comment_form = None         
    else:
        journal = journals[0]
        articles = Article.objects.filter(journal=journal.id).order_by('-created')
        if len(articles) == 0:
            articles = None
            article = None
            earlier = None
            comments = None
            new_comment = None 
            comment_form = None 
        else:
            article = articles[0]
        
            # Статьи ранее
            deep = 3
            earlier = []
            earlier_list = [article]
            while deep != 0:
                deep -= 1
                earlier_tmp = []
                for item in earlier_list:
                    if item.earlier != None:
                        earlier.append(item.earlier)
                        earlier_tmp.append(item.earlier)
                earlier_list = earlier_tmp
            if earlier == []: earlier = [None]
    
            # Список активных комментариев к этой записи  
            comments = article.comments.filter(active=True)  
            new_comment = None  
            if request.method == 'POST':  
                comment_form = CommentForm(data=request.POST)  
                if comment_form.is_valid():  
                    new_comment = comment_form.save(commit=False)  
                    new_comment.article = article
                    #new_comment.ip = request.META.get('REMOTE_ADDR')
                    new_comment.save() 
            else:  
                comment_form = CommentForm()  
                
    context = {}
    context.update({'article': article})
    context.update({'earlier': earlier})
    context.update({'articles': articles})
    context.update({'journal': journal})
    context.update({'journals': journals})
    context.update({'best_week_articles': best_week_articles()})
    context.update({'random_author': random_author()})
    context.update({'random_authors': random_authors()})
    context.update({'comments': comments})
    context.update({'new_comment': new_comment})
    context.update({'comment_form': comment_form})  
    context.update({'last_comments': last_comments()})
    
    return render(request, 'page_journals__list.html', context)
    
def journal(request, year, journal_slug, article_slug=None):
    journals = Journal.objects.filter(year=year).order_by('-index')

    journal = Journal.objects.filter(slug=journal_slug)
    if len(journal) == 0:
        journals = None
        journal = None
        articles = None
        article = None
        earlier = None
        comments = None
        new_comment = None
        comment_form = None
    else:
        journal = journal[0]
        articles = Article.objects.filter(journal=journal.id).order_by('-created')
        
        if len(articles) == 0:
            articles = None
            article = None
            earlier = None
            comments = None
            new_comment = None 
            comment_form = None 
        else:
            if article_slug == None:
                article = articles[0]
            else:
                article = get_object_or_404(Article, slug=article_slug)
        
            # Статьи ранее
            deep = 3
            earlier = []
            earlier_list = [article]
            while deep != 0:
                deep -= 1
                earlier_tmp = []
                for item in earlier_list:
                    if item.earlier != None:
                        earlier.append(item.earlier)
                        earlier_tmp.append(item.earlier)
                earlier_list = earlier_tmp
            if earlier == []: earlier = [None]
    
            # Список активных комментариев к этой записи  
            comments = article.comments.filter(active=True)  
            new_comment = None  
            if request.method == 'POST':  
                comment_form = CommentForm(data=request.POST)  
                if comment_form.is_valid():  
                    new_comment = comment_form.save(commit=False)  
                    new_comment.article = article
                    #new_comment.ip = request.META.get('REMOTE_ADDR')
                    new_comment.save() 
            else:  
                comment_form = CommentForm()  
                
    context = {}
    context.update({'article': article})
    context.update({'earlier': earlier})
    context.update({'articles': articles})
    context.update({'journal': journal})
    context.update({'journals': journals})
    context.update({'best_week_articles': best_week_articles()})
    context.update({'random_author': random_author()})
    context.update({'random_authors': random_authors()})
    context.update({'comments': comments})
    context.update({'new_comment': new_comment})
    context.update({'comment_form': comment_form})  
    context.update({'last_comments': last_comments()})
    
    return render(request, 'page_journals__list.html', context)
    
def tags(request):
    abc = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я'];
    context = {}
    context.update({'abc': abc})
    context.update({'tags': Tag.objects.all()})
    context.update({'articles': articles})
    context.update({'best_week_articles': best_week_articles()})
    context.update({'random_author': random_author()})
    context.update({'random_authors': random_authors()})
    context.update({'last_comments': last_comments()})
    
    return render(request, 'page_tags_all.html', context)
    
def tag(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    articles = Article.objects.filter(tags__in=[tag])

    abc = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я'];
    context = {}
    context.update({'abc': abc})
    context.update({'tag_current': tag})
    context.update({'tags': Tag.objects.all()})
    context.update({'articles': articles})
    context.update({'best_week_articles': best_week_articles()})
    context.update({'random_author': random_author()})
    context.update({'random_authors': random_authors()})
    context.update({'last_comments': last_comments()})
    
    return render(request, 'page_tags_item.html', context)
    
def authors(request):
    authors = Author.objects.order_by('surname', 'name', 'middlename')
    context = {}
    context.update({'authors': authors})
    
    return render(request, 'page_authors.html', context)
    
def author(request, slug):
    author = Author.objects.filter(slug=slug)[0]
    articles = Article.objects.filter(category='article', author=author).order_by('-created')
    
    context = {}
    
    context.update({'author': author})
    context.update({'articles': articles})
    context.update({'best_week_articles': best_week_articles()})
    context.update({'random_author': random_author()})
    context.update({'random_authors': random_authors()})
    context.update({'last_comments': last_comments()})
    
    return render(request, 'page_author__article.html', context)

def search(request):
    context = {}
    query = request.GET.get('q')
    if query:
        articles = Article.objects.filter(
            Q(title__icontains=query) | Q(fulltext__icontains=query)
        )
    else:
        articles = None
        query = ''
        
    context = {}
    context.update({'query': query})
    context.update({'articles': articles})
    context.update({'best_week_articles': best_week_articles()})
    context.update({'random_author': random_author()})
    context.update({'random_authors': random_authors()})
    context.update({'last_comments': last_comments()})
    
    return render(request, 'page_search_result.html', context)
    
def ajax_journals(request, year):
    journals = Journal.objects.filter(year=year).order_by('-index')
    context = {}
    context.update({'journals': journals})
    return render(request, 'ajax_journals.html', context)
    
def ajax_check_year(request, year):
    journals = Journal.objects.filter(year=year).order_by('-index')
    if len(journals) > 0:
        year = True
    else:
        year = False
        
    context = {}
    context.update({'year': year})
    return render(request, 'ajax_check_year.html', context)
    
def ajax_load_category(request, category, article_id, start):
    global CONST_ARTICLES
    global CONST_NEWS
    
    articles = Article.objects.filter(category=category).filter(~Q(id=article_id)).order_by('-created')
    context = {}
    
    if category == 'article':
        context.update({'more_articles': articles[start:start + CONST_ARTICLES]})
        return render(request, 'ajax_load_articles.html', context)
        
    if category == 'news':
        context.update({'more_news': articles[start:start + CONST_NEWS]})
        return render(request, 'ajax_load_news.html', context)
    
def ajax_articles_count(request, category):
    count = len(Article.objects.filter(category=category).order_by('-created'))
    context = {}
    context.update({'count': count})
    return render(request, 'ajax_articles_count.html', context)
    
def page_not_found(request, exception):
    return render(request, 'page_404.html', status=404)