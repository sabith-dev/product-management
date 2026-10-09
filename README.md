# Product Management System

A simple Django-based Product Management System for an e-commerce website, built to demonstrate CRUD operations, authentication, validation, database relationships, UI development, and basic Git workflow.

## Features

- **Authentication**: Login, logout, and registration for users
- **Dashboard**: Overview of total products, active products, inactive products, and low stock products
- **Product Listing**: View all products with search, category filter, status filter, and pagination
- **Add/Edit Product**: Same form for creating and updating products with image upload support
- **Product Details**: View complete product information
- **Delete with Confirmation**: Safe deletion of products
- **Validation**: Form and model-level validation (required fields, unique SKU, positive price, non-negative stock)
- **Business Rules**: Low stock indicator (≤ 5 items), out of stock indicator (0), status display
- **Responsive UI**: Clean, simple interface built with Bootstrap 5

## Technologies Used

- **Backend**: Python 3.13, Django 6.0.3
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **Image Handling**: Pillow

## Project Structure

```
product-management/
├── config/           # Project settings
├── products/         # Main app (models, views, forms, templates, urls)
├── static/           # CSS files
├── media/            # Uploaded product images
├── templates/        # Global templates
├── manage.py
├── seed_data.py      # Sample data script
└── README.md
```

## Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/product-management.git
   cd product-management
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install django pillow
   ```

4. **Apply database migrations**
   ```bash
   python manage.py migrate
   ```

5. **Load sample data (optional)**
   ```bash
   python seed_data.py
   ```

6. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Open your browser and go to `http://127.0.0.1:8000/`
   - Login with your credentials or register a new account

## Login Credentials

You can register a new account via `/register/` or create a superuser using `createsuperuser`. If you loaded seed data, you can also log in with any user you create.

## Usage

1. **Login**: Access the system via the login page
2. **Dashboard**: View product statistics at a glance
3. **Add Product**: Click "Add Product" to create new products
4. **Product List**: View, search, filter, and manage all products
5. **Edit Product**: Update product details using the same form
6. **View Details**: Click "View" to see complete product information
7. **Delete Product**: Remove products with confirmation prompt

## Key Features Implemented

- **Models**: `Category` and `Product` with one-to-many relationship
- **CRUD Operations**: Create, Read, Update, Delete for products
- **Search**: Search by product name or SKU
- **Filters**: Filter by category and status (Active/Inactive)
- **Pagination**: 8 products per page
- **Validation**: SKU uniqueness, required fields, price > 0, stock ≥ 0
- **Authorization**: `@login_required` decorator on add/edit/delete operations
- **Business Rules**: Low stock (< 6 and > 0), out of stock (0)

## Assessment Coverage

This project covers all requirements from the Python/Django Developer Development Test:
- Django basics (models, views, URLs, templates)
- CRUD operations
- Database relationships and ORM
- Clean UI with Bootstrap
- Form validation
- Code organization
- Git workflow with meaningful commits
