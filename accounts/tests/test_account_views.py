import pytest
from django.urls import reverse

@pytest.mark.parametrize(
    "first_name, last_name, phone_number, email, password, confirm_password",
    [
        ("salma","ahmed","01002317789","salma@gmail.com","123456789","123456789"),
    ],
)
@pytest.mark.django_db
def test_register_view_successful(client,first_name, last_name, phone_number, email, password, confirm_password):
    form_data = {
           'first_name': first_name,
           'last_name':last_name,
           'phone_number':phone_number,
           'email':email,
           'password':password,
           'confirm_password':confirm_password
           
        }
    response = client.post(reverse('register'), data=form_data)
    # we redirect the user so we use 302 code that
    assert response.status_code == 302
    
    
    
@pytest.mark.parametrize(
    "first_name, last_name, phone_number, email, password, confirm_password",
    [
        ("salma","ahmed","01002317789","salma@gmail.com","123456789","123456789"),
    ],
)
@pytest.mark.django_db
def test_register_view_email_taken(client,account_factory,first_name, last_name, phone_number, email, password, confirm_password,):
    account_factory.create(email=email)

    form_data = {
           'first_name': first_name,
           'last_name':last_name,
           'phone_number':phone_number,
           'email':email,
           'password':password,
           'confirm_password':confirm_password
           
        }
    response = client.post(reverse('register'), data=form_data)
    assert response.status_code == 200
    # Check if form errors are displayed in the response content
    messages_list = list(response.context['messages'])
    assert len(messages_list) == 1
    assert str(messages_list[0]) == '<ul class="errorlist"><li>Account with this Email already exists.</li></ul>'
    
@pytest.mark.django_db  
def test_register_view_get_method(client):
    response = client.get(reverse('register'))
    assert response.status_code == 200