import secrets
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import json

app = Flask(__name__)

# Rastgele bir JWT secret key oluşturma
app.config['JWT_SECRET_KEY'] = secrets.token_hex(32)  # 32 byte'lık güçlü bir secret key
app.config['TESTING'] = False  # Test sırasında rate limiting'i devre dışı bırakmak için kullanacağız

# JWTManager ile JWT yönetimini etkinleştir
jwt = JWTManager(app)

# Limiter yapılandırması (IP adresine göre sınırlama)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["5 per minute"],  # Varsayılan olarak kullanıcı başına 1 dakikada 5 istek sınırı
    enabled=not app.config.get('TESTING', False)   # Test modunda rate limiting devre dışı bırakılır
)

# Load sample data from JSON files
with open('./json_samples/movies.json', 'r') as f:
    movies = json.load(f)

with open('./json_samples/series.json', 'r') as f:
    series = json.load(f)

# Routes
@app.route('/')
@limiter.limit("10 per minute")  # 1 dakikada 10 istek sınırı
def home():
    return 'Welcome to the Movie and Series API'

# get all movies and series (JWT token gerektirir)
@app.route('/media', methods=['GET'])
@jwt_required()  # Token gereklidir
@limiter.limit("5 per minute")  # 1 dakikada 5 istek sınırı
def get_media():
    return jsonify({'movies': movies, 'series': series})

# authentication (JWT token oluşturur)
@app.route('/login', methods=['POST'])
@limiter.limit("3 per minute")  # 1 dakikada 3 giriş denemesi
def login():
    user = request.get_json()
    if user['username'] == 'admin' and user['password'] == 'admin':
        access_token = create_access_token(identity=user['username'])  # Token oluştur
        return jsonify(access_token=access_token)
    return jsonify({'message': 'Login failed'}), 401

# # Routes for movies (JWT token gerektirir)
@app.route('/movies', methods=['GET'])
@jwt_required()  # Token gereklidir
@limiter.limit("5 per minute")  # 1 dakikada 5 istek sınırı
def get_movies():
    return jsonify(movies)

# add a new movie (JWT token gerektirir)
@app.route('/movies', methods=['POST'])
@jwt_required()  # Token gereklidir
@limiter.limit("3 per minute")  # 1 dakikada 3 film ekleme isteği
def add_movie():
    movie = request.get_json()
    if not movie or 'title' not in movie or 'year' not in movie:
        return jsonify({'error': 'Invalid input'}), 400
    movies.append(movie)
    return jsonify(movie), 201

# get a specific movie (JWT token gerektirir)
@app.route('/movies/<int:id>', methods=['GET'])
@jwt_required()  # Token gereklidir
@limiter.limit("5 per minute")  # 1 dakikada 5 istek sınırı
def get_movie(id):
    return jsonify(movies[id])

# update a specific movie (JWT token gerektirir)
@app.route('/movies/<int:id>', methods=['PUT'])
@jwt_required()  # Token gereklidir
@limiter.limit("3 per minute")  # 1 dakikada 3 güncelleme isteği
def update_movie(id):
    movie = movies[id]
    movie.update(request.get_json())
    return jsonify(movie)

# delete a specific movie (JWT token gerektirir)
@app.route('/movies/<int:id>', methods=['DELETE'])
@jwt_required()  # Token gereklidir
@limiter.limit("3 per minute")  # 1 dakikada 3 silme isteği
def delete_movie(id):
    movie = movies.pop(id)
    return jsonify(movie)

# get top 5 movies (JWT token gerektirir)
@app.route('/movies/top', methods=['GET'])
@jwt_required()  # Token gereklidir
@limiter.limit("5 per minute")  # 1 dakikada 5 istek sınırı
def get_top_movies():
    top_movies = sorted(movies, key=lambda x: x['ratings'], reverse=True)[:5]
    return jsonify(top_movies)

# # Routes for series (JWT token gerektirir)
@app.route('/series', methods=['GET'])
@jwt_required()  # Token gereklidir
@limiter.limit("5 per minute")  # 1 dakikada 5 istek sınırı
def get_series():
    return jsonify(series)

# add a new serie (JWT token gerektirir)
@app.route('/series', methods=['POST'])
@jwt_required()  # Token gereklidir
@limiter.limit("3 per minute")  # 1 dakikada 3 dizi ekleme isteği
def add_series():
    serie = request.get_json()
    if not serie or 'title' not in serie or 'year' not in serie:
        return jsonify({'error': 'Invalid input'}), 400
    series.append(serie)
    return jsonify(serie), 201

# get a specific serie (JWT token gerektirir)
@app.route('/series/<int:id>', methods=['GET'])
@jwt_required()  # Token gereklidir
@limiter.limit("5 per minute")  # 1 dakikada 5 istek sınırı
def get_serie(id):
    return jsonify(series[id])

# update a specific serie (JWT token gerektirir)
@app.route('/series/<int:id>', methods=['PUT'])
@jwt_required()  # Token gereklidir
@limiter.limit("3 per minute")  # 1 dakikada 3 güncelleme isteği
def update_serie(id):
    serie = series[id]
    serie.update(request.get_json())
    return jsonify(serie)

# delete a specific serie (JWT token gereklidir)
@app.route('/series/<int:id>', methods=['DELETE'])
@jwt_required()  # Token gereklidir
@limiter.limit("3 per minute")  # 1 dakikada 3 silme isteği
def delete_serie(id):
    serie = series.pop(id)
    return jsonify(serie)

# get top 5 series (JWT token gerektirir)
@app.route('/series/top', methods=['GET'])
@jwt_required()  # Token gereklidir
@limiter.limit("5 per minute")  # 1 dakikada 5 istek sınırı
def get_top_series():
    top_series = sorted(series, key=lambda x: x['ratings'], reverse=True)[:5]
    return jsonify(top_series)

if __name__ == '__main__':
    app.run(debug=True)