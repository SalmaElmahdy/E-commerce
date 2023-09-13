import pytest
from django.urls import reverse

def test_category_str(category):
    assert category.__str__() == 'django'
    
def test_category_get_url(client,category):
    url = reverse("products_by_category",args=[category])
    response= client.get(url)
    assert response.status_code == 200