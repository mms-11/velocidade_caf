# Velocidade CAF

## Overview

Velocidade CAF is a Progressive Web App (PWA) project that combines a FastAPI backend with a Vite + React + TypeScript frontend. This project structure is designed to facilitate the development of modern web applications with a focus on performance and user experience.

## Project Structure

The project is organized into two main directories: `backend` and `frontend`.

### Backend

The backend is built using FastAPI, a modern web framework for building APIs with Python. The backend directory contains the following:

- **app**: Contains the main application code.
  - **main.py**: Entry point for the FastAPI application.
  - **api**: Contains API versioning and endpoints.
    - **v1**: Version 1 of the API.
      - **endpoints**: Contains individual endpoint definitions.
        - **health.py**: Health check endpoint.
      - **deps.py**: Dependency functions for API routes.
  - **core**: Configuration settings for the application.
    - **config.py**: Application configuration.
  - **models**: Data models for the application.
    - **user.py**: User model definition.
  - **schemas**: Pydantic schemas for request and response validation.
    - **user.py**: User schemas.
  - **services**: Business logic and services.
    - **auth.py**: Authentication services.
  - **__init__.py**: Marks the app directory as a Python package.
- **tests**: Contains unit tests for the application.
  - **test_health.py**: Tests for the health check endpoint.
- **pyproject.toml**: Project metadata and dependencies.
- **requirements.txt**: List of required Python packages.
- **Dockerfile**: Instructions for building a Docker image for the FastAPI application.
- **README.md**: Documentation for the backend.

### Frontend

The frontend is built using Vite, React, and TypeScript, providing a modern development experience. The frontend directory contains the following:

- **package.json**: Configuration file for npm, listing dependencies and scripts.
- **tsconfig.json**: TypeScript configuration file.
- **vite.config.ts**: Vite configuration file.
- **index.html**: Main HTML file for the application.
- **public**: Contains static assets.
  - **manifest.webmanifest**: Web app manifest for PWA.
- **src**: Source code for the React application.
  - **main.tsx**: Entry point for the React application.
  - **App.tsx**: Main App component.
  - **service-worker.ts**: Service worker logic for PWA features.
  - **components**: Contains reusable components.
    - **ExampleComponent.tsx**: Example React component.
  - **pages**: Contains page components.
    - **Home.tsx**: Home page component.
  - **api**: API client setup.
    - **client.ts**: Fetch client for API requests.
  - **styles**: Global styles for the application.
    - **index.css**: CSS styles.
- **.eslintrc.cjs**: ESLint configuration.
- **.prettierrc**: Prettier configuration.
- **README.md**: Documentation for the frontend.

### Docker

The project includes a `docker-compose.yml` file for managing services and configurations for local development using Docker.

### Git

The `.gitignore` file specifies files and directories to be ignored by Git.

## Getting Started

To get started with the Velocidade CAF project, follow these steps:

1. Clone the repository.
2. Navigate to the `backend` directory and install the required Python packages.
3. Navigate to the `frontend` directory and install the required npm packages.
4. Run the backend and frontend applications using Docker or your preferred method.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or features you'd like to add.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.