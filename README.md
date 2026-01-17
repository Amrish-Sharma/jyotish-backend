# Jyotish Backend

High-precision astrology backend system acting as a single source of truth for Kundli generation and astrological calculations.

## Tech Stack

*   **Language**: Python 3.11+
*   **Framework**: FastAPI
*   **Engine**: Swiss Ephemeris (`pyswisseph`)
*   **Caching**: Redis

## Setup

1.  Create a virtual environment:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

2.  Install dependencies:
    ```bash
    pip install .[dev]
    ```

3.  Run the server:
    ```bash
    uvicorn app.main:app --reload
    ```

4.  Run the Frontend:
    ```bash
    cd ui
    npm install
    npm run dev
    ```
    Access the UI at `http://localhost:5173`.
