# Flask API Project

This project is a Flask-based API for managing users and roles. It includes features such as user authentication, role-based access control, and CRUD operations for users.

## Features

- User authentication using JWT tokens.
- Role-based access control.
- CRUD operations for users and roles.
- Pagination, sorting, and filtering for user lists.
- Soft deletion for users.

## Installation

### Prerequisites

- Python 3.8 or higher
- Virtual environment (recommended)

### Steps

1. Clone the repository and navigate to the project directory:

   ```bash
   git clone <repository-url>
   cd flask-api
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   source .venv/bin/activate  # On macOS/Linux
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up the database:

   ```bash
   python seed.py
   ```
   This will create the database and seed it with an admin user and role.

5. Run the application:

   ```bash
   python app.py
   ```
   The application will be available at http://127.0.0.1:5000.

# Seeding Data
The seed.py script initializes the database with the following:

- An admin user with the username admin and password Asdlkj123.
- An "Administrator" role linked to the admin user.

# License
This project is licensed under the MIT License.