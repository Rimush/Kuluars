from django.shortcuts import render
from .models import Settings

def load_settings(request):
    return {'site_settings': Settings.load()}
    
def video_products(request):
    
    context = {}
    
    return render(request, 'page_articles__list.html', context)