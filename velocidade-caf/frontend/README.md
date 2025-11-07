# Frontend README.md

# Frontend Documentation

This project is a Progressive Web App (PWA) built using React, TypeScript, and Vite. It is designed to work seamlessly with a FastAPI backend.

## Project Structure

The frontend directory contains the following key files and folders:

- **package.json**: Contains the project's dependencies and scripts for building and running the application.
- **tsconfig.json**: TypeScript configuration file that specifies compiler options.
- **vite.config.ts**: Configuration file for Vite, which is used for development and building the application.
- **index.html**: The main HTML file that serves as the entry point for the application.
- **public/manifest.webmanifest**: Web app manifest that provides metadata for the PWA.
- **src/**: Contains the source code for the application, including components, pages, and styles.
  - **main.tsx**: Entry point for the React application.
  - **App.tsx**: The main App component.
  - **service-worker.ts**: Service worker logic for enabling PWA features.
  - **components/**: Contains reusable React components.
  - **pages/**: Contains page components for different routes.
  - **api/**: Contains API client setup for making requests to the backend.
  - **styles/**: Contains global styles for the application.
- **.eslintrc.cjs**: ESLint configuration for code linting.
- **.prettierrc**: Prettier configuration for code formatting.

## Getting Started

To get started with the frontend application, follow these steps:

1. Clone the repository:
   ```
   git clone <repository-url>
   ```

2. Navigate to the frontend directory:
   ```
   cd velocidade-caf/frontend
   ```

3. Install the dependencies:
   ```
   npm install
   ```

4. Start the development server:
   ```
   npm run dev
   ```

5. Open your browser and navigate to `http://localhost:3000` to view the application.

## Building for Production

To build the application for production, run:
```
npm run build
```

This will create an optimized build of the application in the `dist` directory.

## PWA Features

This application is a Progressive Web App, which means it can be installed on devices and work offline. The service worker is configured to cache assets and API responses for improved performance.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.