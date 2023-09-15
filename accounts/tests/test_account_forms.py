import pytest

from accounts.forms import RegisterationForm
from django import forms
@pytest.mark.parametrize(
    "first_name, last_name, phone_number, email, password, confirm_password,validaty",
    [
        ("salma","ahmed","01002317789","salma@gmail.com","123456789","123456789",True),
        ("","ahmed","01002317789","salma@gmail.com","123456789","123456789",False),
        ("salma","","01002317789","salma@gmail.com","123456789","123456789",False),
        ("salma","ahmed","01002317789","","123456789","123456789",False),
        ("salma","ahmed","01002317789","salma@gmail.com","123456789","123456",False),
    ],
)
@pytest.mark.django_db
def test_account_register_form(first_name, last_name, phone_number, email, password, confirm_password,validaty):
    form = RegisterationForm(
        data={
           'first_name': first_name,
           'last_name':last_name,
           'phone_number':phone_number,
           'email':email,
           'password':password,
           'confirm_password':confirm_password
           
        }
    )
    assert form.is_valid() == validaty




@pytest.mark.parametrize(
    "first_name, last_name, phone_number, email, password, confirm_password,validaty",
    [
        ("salma","ahmed","01002317789","salma@gmail.com","123456789","1234567",False),
    ],
)
@pytest.mark.django_db
def test_account_register_form_not_match_passwords_exception(first_name, last_name, phone_number, email, password, confirm_password,validaty):
    form = RegisterationForm(
        data={
           'first_name': first_name,
           'last_name':last_name,
           'phone_number':phone_number,
           'email':email,
           'password':password,
           'confirm_password':confirm_password
           
        }
    )
    assert form.is_valid() == validaty
    # cleaned data is populated after is_valid called so i coul not test forms raise exception
    # until adding that call
    with pytest.raises(forms.ValidationError) as e:
        form.clean()

    assert str(e.value) == "['Password does not match.']"