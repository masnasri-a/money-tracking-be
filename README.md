# FastAPI Auth MongoDB with Money Management

## Overview

This project is a FastAPI-based RESTful API that provides authentication, user management, and money management features. It uses MongoDB as the database backend and includes JWT-based authentication.

## Features

- User registration and authentication
- JWT token generation and validation
- User profile management (including profile picture upload)
- Transaction management (create, read, update, delete)
- Monthly spending limit setting and retrieval
- Standardized API responses for consistent client-side handling

## Technologies Used

- FastAPI
- MongoDB (with Motor for asynchronous operations)
- PyJWT for JWT handling
- Pydantic for data validation
- Python 3.8+

## Installation and Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/FastAPI-Auth-MongoDB.git
    cd FastAPI-Auth-MongoDB
    ```

2. Create and activate a virtual environment:
    ```bash
    python3 -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up environment variables:
    Create a `.env` file in the root directory and add the following variables:
    ```
    MONGO_URI=<your_mongodb_uri>
    SECRET_KEY=<your_secret_key>
    ```

5. Run the application:
    ```bash
    uvicorn main:app --reload
    ```

6. Access the API documentation:
    Open your browser and go to `http://127.0.0.1:8000/docs` to see the interactive API documentation.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
