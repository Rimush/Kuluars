from functools import wraps
from django.db.models import F
from django.db import transaction


def counted(f):
    @wraps(f)
    def decorator(request, *args, **kwargs):
        with transaction.atomic():
            counter, created = Article.objects.get_or_create(url=request.path)
            counter.count = F('count') + 1
            counter.save()
        return f(request, *args, **kwargs)
    return decorator