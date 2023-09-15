import pytest

def test_account_str(db,account):
    assert account.first_name is not None
    assert account.last_name is not None
    assert account.username is not None
    assert account.email is not None
    assert account.phone_number is not None
    assert account.__str__() == 'user1@example.com'
    

def test_admin_account(db,admin_account):
    assert admin_account.first_name == 'admin_user'
    assert admin_account.is_superadmin == True

def test_not_exist_email(db,account_factory):
    with pytest.raises(ValueError) as e:
        test = account_factory.create(email="")
        assert str(e.value) == "user must have an email address"

def test_not_valid_email(db,account_factory):
    with pytest.raises(ValueError) as e:
        test = account_factory.create(email="aaa.com")
        assert str(e.value) == "please enter valid email"