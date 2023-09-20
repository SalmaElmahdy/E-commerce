# :handbag: E-Commerce Website with Django 

## :memo:  Description

This is an e-commerce website built using Django, which provides a range of features including user authentication, authorization, email verification, password reset, product management, reviews, ratings, shopping cart, and order history.

## :white_check_mark: Features

### User Authentication and Authorization

- Users can create accounts and log in securely.
- Access to certain features is restricted based on user roles (e.g., regular user, admin).

### Email Verification and Password Reset

- Users receive a verification email upon registration.
- Password reset functionality is available via email.

### Product Management

- Admins can add, edit, and remove products.
- Products can be categorized and displayed accordingly.

### Product Reviews and Ratings

- Users can rate and review products they have purchased.

### User Profile Management

- Users can update their profile information and upload a profile picture.

### Shopping Cart

- Users can add items to their shopping cart.
- Quantity of items in the cart can be adjusted or items can be removed.

### Checkout and Order History

- Users can complete their purchase and view their order history.

## :information_desk_person: Getting Started

1. Clone the repository.
2. Use git bash to activate that environment
3. Set up a virtual environment using `python -m venv env`.
4. Activate the virtual environment:
   - On Windows: `source env/scripts/activate`
   - On macOS and Linux: `source env/bin/activate`
5. Install dependencies using `pip install -r requirements.txt`.
6. Run the development server with `python manage.py runserver`.

## :computer: Usage

1. Create a superuser to access the admin panel by type in terminal: `python manage.py createsuperuser`.
2. Log in to the admin panel at `http://localhost:8000/admin` to manage products and user accounts.
3. create and login to user panel at `http://localhost:8000/` to manage your profile and add items to your cart


  
  


