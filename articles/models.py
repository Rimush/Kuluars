from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from sorl.thumbnail import ImageField
from datetime import datetime
from os.path import splitext
from hashlib import blake2b
from taggit.managers import TaggableManager
from django.utils.text import slugify

def get_name(instance, filename):
    s = str(datetime.now().timestamp()) + filename
    h = blake2b(digest_size=4)
    h.update(s.encode('utf-8'))
    h = h.hexdigest()
    
    return '%s_%s%s' % (splitext(filename)[0], h, splitext(filename)[1])

class Author(models.Model):
    surname = models.CharField(max_length=256, verbose_name='Фамилия')
    name = models.CharField(max_length=256, verbose_name='Имя')
    middlename = models.CharField(max_length=256, verbose_name='Отчество')
    image = models.ImageField(verbose_name='Фотография', upload_to='authors')
    slug = models.SlugField(verbose_name='Алиас', unique=True, blank=True, max_length=100)
    
    def save(self):
        super(Author, self).save()
        if not self.slug:
            self.slug = slugify(self.surname) + '-' + slugify(self.name) + '-' + str(self.id)
            super(Author, self).save()
            
    class Meta:
        verbose_name_plural = 'Авторы'
        verbose_name = 'автора'
        
    def __str__(self):
        return f"{self.surname} {self.name} {self.middlename}"
        
class Article(models.Model):
    CATEGORIES = (
        ('article', 'Статьи'),
        ('news', 'Новости'),
    )

    category = models.CharField(max_length=10, verbose_name='Категория', choices=CATEGORIES)
    author = models.ForeignKey(Author, verbose_name='Автор', on_delete=models.CASCADE, null=True, blank=True)
    source = models.CharField(max_length=256, verbose_name='Источник', blank=True)
    important = models.BooleanField(verbose_name='Главное')
    image = models.ImageField(verbose_name='Изображение', upload_to='image')
    image_signature = models.CharField(max_length=256, verbose_name='Подпись изображения')
    title = models.CharField(max_length=256, verbose_name='Заголовок')
    slug = models.SlugField(verbose_name='Алиас', unique=True, blank=True, max_length=100)
    fulltext = RichTextUploadingField(verbose_name='Полный текст')
    #fulltext = models.TextField(verbose_name='Полный текст')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    earlier = models.ForeignKey('self', verbose_name='Ранее', on_delete=models.CASCADE, null=True, blank=True) 
    tags = TaggableManager(blank=True)
    views = models.PositiveIntegerField(verbose_name='Просмотры', default=0)
    
    def save(self):
        super(Article, self).save()
        if not self.slug:
            self.slug = slugify(self.title, True) + '-' + str(self.id)
            super(Article, self).save()
            
    class Meta:
        verbose_name_plural = 'Статьи'
        verbose_name = 'статью'
        
    def __str__(self):
        #return f"{self.title} | {self.fulltext[:100]}..."
        return f"{self.title}"
        
class Journal(models.Model):
    name = models.CharField(max_length=256)
    
    def save(self):
        super(Journal, self).save()
            
    class Meta:
        verbose_name_plural = 'Журналы'
        verbose_name = 'журнал'
        
    def __str__(self):
        return f"{self.name}"