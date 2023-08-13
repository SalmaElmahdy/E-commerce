# we use this file to make that data available accross all the templates
# it takes a request and return a dictionary of data
# and it should add to settings
from .models import Category


def menu_links(request):
    links=Category.objects.all()
    return dict(links=links)