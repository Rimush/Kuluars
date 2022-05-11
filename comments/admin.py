from django.contrib import admin
from .models import Comment

class CommentsAdmin(admin.ModelAdmin):
    list_display = ('name', 'article', 'content', 'created')
    list_display_links = ('name', 'article', 'content', 'created', )
    search_fields = ('content', )
    '''formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget}
    }'''
    
# Register your models here.
admin.site.register(Comment, CommentsAdmin)


