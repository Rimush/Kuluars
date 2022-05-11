from django.contrib import admin
from .models import Article, Author, Journal
    
class AuthorAdmin(admin.ModelAdmin):
    ordering = ['surname', 'name', 'middlename', ]
    search_fields = ['surname', 'name', 'middlename', ]  
    
class ArticlesAdmin(admin.ModelAdmin):
    autocomplete_fields = ['author', 'earlier', ]
    list_display = ('title', 'author', 'category', 'created')
    list_display_links = ('title',)
    search_fields = ('title', )
    '''formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget}
    }'''
    
class JournalAdmin(admin.ModelAdmin):
    ordering = ['name', ]
    search_fields = ['name', ]  
    
# Register your models here.
#admin.site.register(Сategory)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Article, ArticlesAdmin)
admin.site.register(Journal, JournalAdmin)


