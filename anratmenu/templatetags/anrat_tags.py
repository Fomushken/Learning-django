from django import template
from django.db.models import Count

import anratmenu.views as views
from anratmenu.models import Categories, TagDrink

register = template.Library()


@register.inclusion_tag('anratmain/list_categories.html')
def show_categories(cat_selected=0):
    return {'cats': Categories.objects.annotate(total=Count("drinks")).filter(total__gt=0), 'cat_selected': cat_selected}


@register.inclusion_tag('anratmain/list_tags.html')
def show_all_tags():
    return {'tags': TagDrink.objects.annotate(total=Count("drinks")).filter(total__gt=0)}