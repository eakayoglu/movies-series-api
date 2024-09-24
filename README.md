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

4. Create `movies.json` and `series.json` files in the root directory with the following content:

    **movies.json**
    ```json
    [
        {"title": "The Godfather", "year": 1972, "genre": "Crime", "ratings": 9.2, "director": "Francis Ford Coppola"},
        {"title": "The Shawshank Redemption", "year": 1994, "genre": "Drama", "ratings": 9.3, "director": "Frank Darabont"},
        {"title": "The Dark Knight", "year": 2008, "genre": "Action", "ratings": 9.0, "director": "Christopher Nolan"},
        {"title": "Pulp Fiction", "year": 1994, "genre": "Crime", "ratings": 8.9, "director": "Quentin Tarantino"},
        {"title": "Forrest Gump", "year": 1994, "genre": "Drama", "ratings": 8.8, "director": "Robert Zemeckis"},
        {"title": "Inception", "year": 2010, "genre": "Sci-Fi", "ratings": 8.8, "director": "Christopher Nolan"},
        {"title": "Fight Club", "year": 1999, "genre": "Drama", "ratings": 8.8, "director": "David Fincher"},
        {"title": "The Matrix", "year": 1999, "genre": "Sci-Fi", "ratings": 8.7, "director": "Lana Wachowski, Lilly Wachowski"},
        {"title": "Goodfellas", "year": 1990, "genre": "Crime", "ratings": 8.7, "director": "Martin Scorsese"},
        {"title": "The Lord of the Rings: The Return of the King", "year": 2003, "genre": "Fantasy", "ratings": 8.9, "director": "Peter Jackson"}
    ]
    ```

    **series.json**
    ```json
    [
        {"title": "Breaking Bad", "year": 2008, "genre": "Crime", "ratings": 9.5, "director": "Vince Gilligan"},
        {"title": "Game of Thrones", "year": 2011, "genre": "Fantasy", "ratings": 9.3, "director": "David Benioff, D.B. Weiss"},
        {"title": "The Sopranos", "year": 1999, "genre": "Crime", "ratings": 9.2, "director": "David Chase"},
        {"title": "Sherlock", "year": 2010, "genre": "Crime", "ratings": 9.1, "director": "Mark Gatiss, Steven Moffat"},
        {"title": "Friends", "year": 1994, "genre": "Comedy", "ratings": 8.9, "director": "David Crane, Marta Kauffman"},
        {"title": "The Office", "year": 2005, "genre": "Comedy", "ratings": 8.9, "director": "Greg Daniels, Ricky Gervais, Stephen Merchant"},
        {"title": "Stranger Things", "year": 2016, "genre": "Drama", "ratings": 8.7, "director": "Matt Duffer, Ross Duffer"},
        {"title": "The Mandalorian", "year": 2019, "genre": "Sci-Fi", "ratings": 8.8, "director": "Jon Favreau"},
        {"title": "The Crown", "year": 2016, "genre": "Drama", "ratings": 8.7, "director": "Peter Morgan"},
        {"title": "Westworld", "year": 2016, "genre": "Sci-Fi", "ratings": 8.6, "director": "Jonathan Nolan, Lisa Joy"}
    ]
    ```

5. Run the application:
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


