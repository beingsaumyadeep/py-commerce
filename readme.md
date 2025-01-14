# E-Commerce Application

This is a Python-based e-commerce application built with FastAPI, SQLAlchemy, and Redis for session management. This README provides instructions on how to set up, install, and run the application.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [License](#license)

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.8 or higher
- PostgreSQL for the database
- Redis for session management
- pip for package management

## Installation

1. **Clone the repository:**

   ````bash
   git clone https://github.com/yourusername/ecommerce.git
   cd ecommerce```

   ````

2. **Set up a virtual environment:**

   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**

- On macOS/Linux:

  ```bash
  source venv/bin/activate
  ```

- On Windows:

  ```bash
  venv\Scripts\activate
  ```

4. **Install the required packages:**

   ```bash
   pip install -r requirements.txt
   ```

5. **Configuration:**

   Create a .env file in the root of your project and add the following environment variables:

   ```plaintext
   DATABASE_URL="postgresql://username:password@host:port/database"
   ANTROPIC_API="your_antropic_api_key"
   REDIS_DB="rediss://username:password@host:port"
   REDIS_HOST="your_redis_host"
   REDIS_PORT=your_redis_port
   REDIS_USER="your_redis_username"
   REDIS_PASS="your_redis_password"
   ```

   Modify the database URL with your PostgreSQL credentials.

6. **Running the Application:**

   Start the application:

   ```bash
   uvicorn main:app --reload
   ```

   The application will be available at http://127.0.0.1:8000.

   Access the API documentation: Open your browser and go to http://127.0.0.1:8000/docs to view the interactive API documentation provided by FastAPI.

## API Endpoints

- User Registration: POST /users/
- User Login: POST /login
- Get Current User: GET /users/me

## License

This project is licensed under the MIT License - see the LICENSE file for details.