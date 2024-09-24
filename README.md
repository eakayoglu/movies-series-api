# Movie - Series API

This project is a RESTful API built with Flask that allows users to manage a collection of movies and series. The API supports CRUD operations and includes JWT-based authentication and rate limiting.

- JWT Authentication
- Rate Limiting
- CRUD operations for Movies and Series
- Top 5 Movies and Series based on ratings

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Endpoints](#endpoints)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/eakayoglu/movies-series-api.git
    cd movies-series-api
    ```

2. Create a virtual environment and activate it:
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```


4. Run the application:
    ```sh
    flask run
    ```

## Usage

The API provides endpoints to manage movies and series. You can use tools like `curl` or Postman to interact with the API.

## Endpoints

### Authentication

- **POST /login**: Authenticate and get a JWT token.
    - Request body:
        ```json
        {
            "username": "admin",
            "password": "admin"
        }
        ```
    - Response:
        ```json
        {
            "access_token": "your_jwt_token"
        }
        ```

### Movies

- **GET /movies**: Get all movies (requires JWT token).
- **POST /movies**: Add a new movie (requires JWT token).
    - Request body:
        ```json
        {
            "title": "New Movie",
            "year": 2024,
            "genre": "Drama",
            "ratings": 9.1,
            "director": "John Doe"
        }
        ```
- **GET /movies/<int:id>**: Get a specific movie by ID (requires JWT token).
- **PUT /movies/<int:id>**: Update a specific movie by ID (requires JWT token).
    - Request body:
        ```json
        {
            "ratings": 9.5
        }
        ```
- **DELETE /movies/<int:id>**: Delete a specific movie by ID (requires JWT token).
- **GET /movies/top**: Get top 5 movies (requires JWT token).

### Series

- **GET /series**: Get all series (requires JWT token).
- **POST /series**: Add a new series (requires JWT token).
    - Request body:
        ```json
        {
            "title": "Dark",
            "year": 2017,
            "genre": "Sci-Fi",
            "ratings": 8.8,
            "director": "Baran bo Odar"
        }
        ```
- **GET /series/<int:id>**: Get a specific series by ID (requires JWT token).
- **PUT /series/<int:id>**: Update a specific series by ID (requires JWT token).
    - Request body:
        ```json
        {
            "ratings": 9.6
        }
        ```
- **DELETE /series/<int:id>**: Delete a specific series by ID (requires JWT token).
- **GET /series/top**: Get top 5 series (requires JWT token).

### Rate Limiting

- **/login**: 3 requests per minute
- **/**: 10 requests per minute
- **/media**: 5 requests per minute
- **/movies**: 5 requests per minute
- **/movies (POST)**: 3 requests per minute
- **/movies/<int:id> (PUT/DELETE)**: 3 requests per minute
- **/movies/top**: 5 requests per minute
- **/series**: 5 requests per minute
- **/series (POST)**: 3 requests per minute
- **/series/<int:id> (PUT/DELETE)**: 3 requests per minute
- **/series/top**: 5 requests per minute

## Testing

To run the tests, use the following command:
```sh
pytest -v -s --tb=auto test_app.py


Sample Output:
```sh
============================= test session starts ==============================
platform darwin -- Python 3.11.3, pytest-8.3.2, pluggy-1.5.0 -- /Library/Frameworks/Python.framework/Versions/3.11/bin/python3.11
cachedir: .pytest_cache
rootdir: /
plugins: anyio-4.4.0, Faker-28.1.0
collected 16 items                                                             

test_app.py::test_home PASSED
test_app.py::test_login_success PASSED
test_app.py::test_login_fail PASSED
test_app.py::test_get_movies PASSED
test_app.py::test_add_movie PASSED
test_app.py::test_rate_limit_login PASSED
test_app.py::test_get_specific_movie PASSED
test_app.py::test_update_movie PASSED
test_app.py::test_delete_movie PASSED
test_app.py::test_get_top_movies PASSED
test_app.py::test_get_series PASSED
test_app.py::test_add_series PASSED
test_app.py::test_get_specific_series PASSED
test_app.py::test_update_series PASSED
test_app.py::test_delete_series PASSED
test_app.py::test_get_top_series PASSED
```
