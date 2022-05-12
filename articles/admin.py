from django.contrib import admin
from .models import Article, Author, Journal
    
class AuthorAdmin(admin.ModelAdmin):
    ordering = ['surname', 'name', 'middlename', ]
    search_fields = ['surname', 'name', 'middlename', ]  
    
class ArticlesAdmin(admin.ModelAdmin):
    autocomplete_fields = ['author', 'earlier', 'journal', ]
    list_display = ('title', 'author', 'category', 'created')
    list_display_links = ('title',)
    search_fields = ('title', )
    
class JournalAdmin(admin.ModelAdmin):
    ordering = ['-index', ]
    search_fields = ['title', ]  
    
# Register your models here.
admin.site.register(Author, AuthorAdmin)
admin.site.register(Article, ArticlesAdmin)
admin.site.register(Journal, JournalAdmin)


