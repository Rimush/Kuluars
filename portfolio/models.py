from django.db import models
from core.SingletonModel import SingletonModel
from django.utils.translation import ugettext_lazy as _

class Video_products(models.Model):
    title = models.CharField(verbose_name='Заголовок', max_length=256)
    
    def save(self):
        super(Video_products, self).save()
            
    class Meta:
        verbose_name_plural = 'Видео продукция'
        verbose_name = 'видео продукцию'
        
    def __str__(self):
        return f"{self.title}"
        
class Polygraphy(models.Model):
    title = models.CharField(verbose_name='Заголовок', max_length=256)
    
    def save(self):
        super(Polygraphy, self).save()
            
    class Meta:
        verbose_name_plural = 'Полиграфия'
        verbose_name = 'полиграфию'
        
    def __str__(self):
        return f"{self.title}" 
        
class Work_in_elections(models.Model):
    title = models.CharField(verbose_name='Заголовок', max_length=256)
    
    def save(self):
        super(Work_in_elections, self).save()
            
    class Meta:
        verbose_name_plural = 'Работа на выборах'
        verbose_name = 'работу на выборах'
        
    def __str__(self):
        return f"{self.title}" 

class Settings(SingletonModel):
    site_url = models.URLField(verbose_name=_('Website url'), max_length=256)
    title = models.CharField(verbose_name=_('Title'), max_length=256)
 
    def __str__(self):
        return 'Configuration'