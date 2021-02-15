from django.core.cache import cache
from django import template
from news.models import Category
# from dja.models import Category,
from django.db.models import Count,F
register=template.Library()
@register.simple_tag(name="get_list_categories")
def get_categories():
    return Category.objects.all()
@register.inclusion_tag('news/list_categories.html')
def show_categories(arg1='hello',arg2='world'):
    categories=cache.get('categories')
    if not categories:

    # categories= Category.objects.all()
        categories = Category.objects.anotate(cnt=Count('news',filter=F(
        'news__is_published'
    ))).filter(cnt__gt=0)
        cache.set('categories',categories,30)

    return {"categories":categories,'arg1':arg1,'arg2':arg2}
