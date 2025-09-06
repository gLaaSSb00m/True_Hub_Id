# Django Website Project

This is a Django-based website project featuring user registration, login, profile management, and an admin panel for user management.

## Features

- User registration with redirect to login page
- User login with authentication
- Profile picture upload with image compression
- Admin panel with user status filtering and management
- Modern UI with animations and responsive design
- Password visibility toggle on login and registration forms

## Screenshots

### Admin Panel - User Management

![Admin Panel](django_website/Asset/admin.png)

### User Registration Page

![Register Page](django_website/Asset/register.png)

### User Login Page

![Login Page](django_website/Asset/login.png)

### User Profile Page

![User Profile](django_website/Asset/user.png)

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd django_website
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Apply migrations:

```bash
python manage.py migrate
```

5. Run the development server:

```bash
python manage.py runserver
```

6. Open your browser and navigate to `http://127.0.0.1:8000/`

## Usage

- Register a new user via the Register page.
- Login with your credentials.
- Access the Admin Panel (if you have admin privileges) to manage users.

## Notes

- Make sure to add the `screenshots` folder with the referenced images before pushing to GitHub.
- Update the repository URL in the clone command above.

## License

This project is licensed under the MIT License.
