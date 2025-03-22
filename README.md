# Online Food Delivery Project Backend

## Project Description

**Project Name**: Online Food Delivery Project

## Overview

The **Online Food Delivery** Project Backend provides a robust platform for viewing and managing food items of different restaurants. Built with **Django** and **Django REST Framework**, it allows for seamless interaction between `owner` and `user`.

Additionally, the use of **PostgreSQL** ensures reliable data handling and scalability, while maintaining flexibility for future enhancements.

---

<br>

## Technology Stack

- **Backend Framework**: Django, Django REST Framework
- **Database**: PostgreSQL (with supabase deployment)

---

<br>

## Project Features

### User Authentication

- User roles: `owners` and `users`.
- Users can `register` for an account and `log in`.
- Users can `log out`.

---

<br>

## Instructions to Run Locally

### Prerequisites

- Python 3.12.2
- Django 4.2.4
- Django REST Framework 3.15.2
- PostgreSQL

### Packages used:

```bash
asgiref==3.8.1
attrs==25.3.0
certifi==2025.1.31
charset-normalizer==3.4.1
dj-database-url==2.3.0
Django==5.1.7
django-cors-headers==4.7.0
django-environ==0.12.0
djangorestframework==3.15.2
djangorestframework_simplejwt==5.5.0
drf-spectacular==0.28.0
idna==3.10
inflection==0.5.1
jsonschema==4.23.0
jsonschema-specifications==2024.10.1
pillow==11.1.0
psycopg2==2.9.10
psycopg2-binary==2.9.10
PyJWT==2.9.0
PyYAML==6.0.2
referencing==0.36.2
requests==2.32.3
rpds-py==0.23.1
sqlparse==0.5.3
sslcommerz-lib==1.0
typing_extensions==4.12.2
tzdata==2025.1
uritemplate==4.1.1
urllib3==2.3.0
```

---

<br>

### Installation Steps

1. Open `command prompt` in the folder directory where you want to create & run the project locally

2. Copy the `repository_url` to **Clone the repository**

   ```bash
   git clone https://github.com/sayed8901/online_food_delivery_django_project.git
   cd online_food_delivery_django_project
   ```

3. **Create a virtual environment**

   ```bash
   python -m venv venv
   cd venv
   Scripts\activate.bat
   cd ..
   ```

4. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   code .
   ```

<br>

5. **Environment Variables Configuration**

- `N.B.`: To run the application, you need to configure environment variables. Create a file named `.env` inside the root project directory of your project.

<br>


6. **Apply migrations**

```bash
python manage.py makemigrations
python manage.py migrate
```

7. **Creating superuser**

```bash
python manage.py createsuperuser
```

8. **Run the development server**

```bash
python manage.py runserver
```

<br>

**Finally, Access the application**

- Local: http://127.0.0.1:8000/
- Admin Panel: http://127.0.0.1:8000/admin/login/

---


<br>

## Getting Started

To unlock and access the full functionality of this site and to perform some role-specific activities, you will need to create an account first. 

---

<br>

## API Endpoints

For API endpoints, check out the [Swagger API documentation](https://online-food-delivery-9i3g.onrender.com/api/schema/swagger-ui/#/).


---

<br>

## Conclusion

I am excited to see the positive impact this system can bring, and if you have any questions or would like to contribute, feel free to reach out!
