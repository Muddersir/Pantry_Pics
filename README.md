🛒 Pantry Pics Grocery Shop – Backend API

A scalable Django + Django REST Framework (DRF) based backend for an online grocery shop. This project supports user authentication, role-based access (admin/seller/customer), product management, cart & wallet system, orders & checkout, and seller dashboards. The backend is designed to be consumed by a React frontend.

🚀 Features
🔐 Authentication & Accounts

Custom User model

Email verification & password reset

JWT authentication

Role-based permissions (Admin / Seller / Customer)

User profile management

📦 Products

Product & category management

Product filtering & search

Wishlist support

Reviews & ratings

🛒 Cart & Wallet

Add/remove items from cart

Wallet / deposit system

Balance tracking

📑 Orders

Checkout system

Balance deduction

Order history

Seller-specific order tracking

Order confirmation emails

📊 Seller Dashboard

Seller product list

Seller orders & earnings overview

🗂 Project Structure
grocery_shop/
├── accounts/     # Authentication & user management
├── products/     # Products, categories, reviews
├── cart/         # Cart & wallet logic
├── orders/       # Orders & checkout
├── seller/       # Seller dashboard APIs
├── utils/        # Shared utilities (email, permissions)
├── static/
├── grocery_shop/ # Project settings
└── manage.py
⚙️ Tech Stack

Backend: Django, Django REST Framework

Auth: JWT (SimpleJWT)

Database: PostgreSQL (recommended) / SQLite (dev)

Email: SMTP (Gmail / SendGrid)

Frontend: React (planned)

🛠 Installation & Setup
1️⃣ Clone the repository
git clone https://github.com/your-username/grocery_shop.git
cd grocery_shop
2️⃣ Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
3️⃣ Install dependencies
pip install -r requirements.txt
4️⃣ Configure environment variables

Create a .env file:

SECRET_KEY=your_secret_key
DEBUG=True
DB_NAME=grocery_db
DB_USER=postgres
DB_PASSWORD=postgres
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
5️⃣ Run migrations
python manage.py makemigrations
python manage.py migrate
6️⃣ Create superuser
python manage.py createsuperuser
7️⃣ Run the server
python manage.py runserver
🔗 API Usage

Base URL: http://127.0.0.1:8000/api/

Auth APIs: /accounts/

Products: /products/

Cart: /cart/

Orders: /orders/

Seller Dashboard: /seller/

Swagger / Postman collection recommended for testing.


📜 License

This project is licensed under the MIT License.

✨ Author

Developed by Muddersir Fiyez