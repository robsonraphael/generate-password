from app.utils.password import generate_password
import pytest

def test_password_generate():
    password = generate_password(10, True, True, True, True)
    
    assert len(password) == 10
    assert any(c.isupper() for c in password)   # capslock
    assert any(c.islower() for c in password)   # minusculo
    assert any(c.isdigit() for c in password)   # digitos
    assert any(not c.isalnum() for c in password)   # simbolos

def test_password_generate_exclude_chars():
    password = generate_password(10, True, True, True, True, exclude_chars="=+!@")
    assert all(c not in "=+!@" for c in password)

def test_generate_password_too_short():
    with pytest.raises(Exception):
        generate_password(3, True, True, True, True)