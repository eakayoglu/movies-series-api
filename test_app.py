# pytest -v -s --tb=auto test_app.py 

import pytest
import json
from app import app, limiter

@pytest.fixture
def client():
    app.config['TESTING'] = True  # Test modunu etkinleştir
    app.config['JWT_SECRET_KEY'] = 'your_static_secret_key'  # Test için sabit bir JWT secret key kullan
    limiter.enabled = False  # Test sırasında rate limiting devre dışı bırakıldı
    with app.test_client() as client:
        yield client

@pytest.fixture
def auth_token(client):
    """Geçerli bir JWT token'ı döndürür"""
    response = client.post('/login', data=json.dumps({
        'username': 'admin',
        'password': 'admin'
    }), content_type='application/json')
    assert response.status_code == 200  # Başarılı giriş kontrolü
    return response.get_json()['access_token']

def test_home(client):
    """Ana sayfanın çalışıp çalışmadığını kontrol eder"""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome to the Movie and Series API" in response.data

def test_login_success(client):
    """Doğru kullanıcı adı ve parola ile giriş yapar"""
    response = client.post('/login', data=json.dumps({
        'username': 'admin',
        'password': 'admin'
    }), content_type='application/json')
    assert response.status_code == 200
    assert 'access_token' in response.get_json()

def test_login_fail(client):
    """Yanlış kullanıcı adı veya parola ile giriş yapmayı dener"""
    response = client.post('/login', data=json.dumps({
        'username': 'wrong',
        'password': 'wrong'
    }), content_type='application/json')
    assert response.status_code == 401
    assert response.get_json() == {'message': 'Login failed'}

def test_get_movies(client, auth_token):
    """Geçerli JWT token ile tüm filmleri almayı test eder"""
    response = client.get('/movies', headers={
        'Authorization': f'Bearer {auth_token}'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)

def test_add_movie(client, auth_token):
    """Geçerli JWT token ile yeni bir film eklemeyi test eder"""
    new_movie = {
        'title': 'New Movie',
        'year': 2024,
        'genre': 'Drama',
        'ratings': 9.1,
        'director': 'John Doe'
    }
    response = client.post('/movies', headers={
        'Authorization': f'Bearer {auth_token}'
    }, data=json.dumps(new_movie), content_type='application/json')
    assert response.status_code == 201
    data = response.get_json()
    assert data['title'] == 'New Movie'

def test_rate_limit_login(client):
    """Rate limiting kontrolü: bir dakika içinde çok fazla giriş denemesi yapıldığında 429 hatası alır"""
    app.config['TESTING'] = False  # Test sırasında rate limiting etkinleştir
    limiter.enabled = True  # Rate limiting'i etkinleştiriyoruz
    
    try:
        # İlk 3 deneme başarılı olmalı
        for _ in range(3):
            response = client.post('/login', data=json.dumps({
                'username': 'admin',
                'password': 'admin'
            }), content_type='application/json')
            assert response.status_code == 200

        # 4. denemede rate limit hatası alır
        response = client.post('/login', data=json.dumps({
            'username': 'admin',
            'password': 'admin'
        }), content_type='application/json')
        assert response.status_code == 429  # Too Many Requests

    finally:
        app.config['TESTING'] = True  # Test modunu geri getir
        limiter.enabled = False  # Testler sırasında rate limiting'i tekrar devre dışı bırak

def test_get_specific_movie(client, auth_token):
    """Geçerli JWT token ile belirli bir filmi almayı test eder"""
    response = client.get('/movies/0', headers={
        'Authorization': f'Bearer {auth_token}'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['title'] == 'The Godfather'  # İlk film 'The Godfather' olmalı

def test_update_movie(client, auth_token):
    """Geçerli JWT token ile belirli bir filmi güncellemeyi test eder"""
    update_data = {'ratings': 9.5}
    response = client.put('/movies/0', data=json.dumps(update_data), headers={
        'Authorization': f'Bearer {auth_token}'
    }, content_type='application/json')
    assert response.status_code == 200
    data = response.get_json()
    assert data['ratings'] == 9.5

def test_delete_movie(client, auth_token):
    """Geçerli JWT token ile belirli bir filmi silmeyi test eder"""
    response = client.delete('/movies/0', headers={
        'Authorization': f'Bearer {auth_token}'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['title'] == 'The Godfather'

def test_get_top_movies(client, auth_token):
    """Geçerli JWT token ile en iyi 5 filmi almayı test eder"""
    response = client.get('/movies/top', headers={
        'Authorization': f'Bearer {auth_token}'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) <= 5  # En fazla 5 film döner
    assert data[0]['ratings'] >= data[-1]['ratings']  # Sıralama kontrolü

def test_get_series(client, auth_token):
    """Geçerli JWT token ile tüm dizileri almayı test eder"""
    response = client.get('/series', headers={
        'Authorization': f'Bearer {auth_token}'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)

def test_add_series(client, auth_token):
    """Geçerli JWT token ile yeni bir dizi eklemeyi test eder"""
    new_series = {
        'title': 'Dark',
        'year': 2017,
        'genre': 'Sci-Fi',
        'ratings': 8.8,
        'director': 'Baran bo Odar'
    }
    response = client.post('/series', data=json.dumps(new_series), headers={
        'Authorization': f'Bearer {auth_token}'
    }, content_type='application/json')
    assert response.status_code == 201
    assert response.get_json() == new_series

def test_get_specific_series(client, auth_token):
    """Geçerli JWT token ile belirli bir diziyi almayı test eder"""
    response = client.get('/series/0', headers={
        'Authorization': f'Bearer {auth_token}'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['title'] == 'Breaking Bad'  # İlk dizi 'Breaking Bad' olmalı

def test_update_series(client, auth_token):
    """Geçerli JWT token ile belirli bir diziyi güncellemeyi test eder"""
    update_data = {'ratings': 9.6}
    response = client.put('/series/0', data=json.dumps(update_data), headers={
        'Authorization': f'Bearer {auth_token}'
    }, content_type='application/json')
    assert response.status_code == 200
    data = response.get_json()
    assert data['ratings'] == 9.6

def test_delete_series(client, auth_token):
    """Geçerli JWT token ile belirli bir diziyi silmeyi test eder"""
    response = client.delete('/series/0', headers={
        'Authorization': f'Bearer {auth_token}'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['title'] == 'Breaking Bad'

def test_get_top_series(client, auth_token):
    """Geçerli JWT token ile en iyi 5 diziyi almayı test eder"""
    response = client.get('/series/top', headers={
        'Authorization': f'Bearer {auth_token}'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) <= 5  # En fazla 5 dizi döner
    assert data[0]['ratings'] >= data[-1]['ratings']  # Sıralama kontrolü