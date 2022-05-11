from django.db import models
from articles.models import Article

class Comment(models.Model):
    article = models.ForeignKey(Article, verbose_name='Статья', on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(verbose_name='Имя', max_length=80)  
    content = models.TextField('Комментарий')
    created = models.DateTimeField(verbose_name='Дата', auto_now_add=True)  
    updated = models.DateTimeField(auto_now=True)  
    active = models.BooleanField(default=True) 
 
    class Meta:
        verbose_name_plural = 'Комментарии'
        verbose_name = 'коментарий'
        ordering = ('created',)  
          
    def __str__(self):  
        return 'Comment by {} on {}'.format(self.name, self.article)