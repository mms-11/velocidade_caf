# Velocidade CAF Backend

This is the backend part of the Velocidade CAF project, which is built using FastAPI. The backend serves as an API for the frontend application, providing endpoints for various functionalities.

## Project Structure

The backend is organized into several directories:

- **app**: Contains the main application code.
  - **api**: Contains the API routes and dependencies.
    - **v1**: Version 1 of the API.
      - **endpoints**: Contains the endpoint definitions.
      - **deps.py**: Dependency functions for the API.
  - **core**: Contains configuration settings for the application.
  - **models**: Contains the data models used in the application.
  - **schemas**: Contains Pydantic schemas for request and response validation.
  - **services**: Contains business logic related to authentication and other services.
- **tests**: Contains unit tests for the application.
- **pyproject.toml**: Configuration file for the Python project.
- **requirements.txt**: Lists the required Python packages.
- **Dockerfile**: Instructions for building a Docker image for the FastAPI application.

## Getting Started

To get started with the backend, follow these steps:

1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd velocidade-caf/backend
   ```

2. **Install dependencies**:
   You can install the required dependencies using pip:
   ```
   pip install -r requirements.txt
   ```

3. **Run the application**:
   You can run the FastAPI application using:
   ```
   uvicorn app.main:app --reload
   ```

4. **Access the API**:
   The API will be available at `http://localhost:8000`. You can access the documentation at `http://localhost:8000/docs`.

## Testing

To run the tests, you can use:
```
pytest
```

## Docker

To build and run the application using Docker, use the following commands:
```
docker build -t velocidade-caf-backend .
docker run -p 8000:8000 velocidade-caf-backend
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.