# Jyotish Graph UI

React-based frontend for the Jyotish Backend, built with Vite.

## Features
*   **Birth Details Input**: City search with timezone resolution.
*   **Kundli Chart**: North Indian (Diamond) chart visualization.
*   **Planetary Data**: Longitudes, signs, retrograde status.
*   **Vimshottari Dasha**: Hierarchical timeline of celestial periods (Mahadasha & Antardasha).
*   **Cosmic Theme**: Custom dark mode styling.

## Setup

1.  **Install Dependencies**:
    ```bash
    npm install
    ```
    *Note: This project uses React 18 and Vite 5 for compatibility with Node.js 18+.*

2.  **Run Development Server**:
    ```bash
    npm run dev
    ```
    The app will start at `http://localhost:5173`.

## Configuration
The app is configured to proxy API requests (`/api/*`) to the backend running at `http://localhost:8000`. Ensure the backend is running before using the frontend.
