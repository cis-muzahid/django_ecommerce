# Django E-commerce Web Application

## Overview

This E-commerce web application is built using Django, providing a robust platform for online shopping. It's designed to handle various aspects of an E-commerce business, including product management, order processing, delivery tracking, and payment gateway integration.

## Features

- **User-Friendly Interface**: Utilizes a main website template tailored for end-users or customers, ensuring an intuitive shopping experience.
  
- **Admin Dashboard**: Incorporates an admin lab template to facilitate efficient management of products, orders, and users.

- **Role-Based Access Control**: Implements multiple roles and permissions to govern user access and responsibilities within the platform.

## Technologies Used

- **Backend**: Django
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Database**: PostgreSQL
- **Payment Gateway**: Stripe
- **Delivery**: Integration with delivery services
- **Templates**: Main website template for end-users, Admin lab template for management

## Installation and Setup

1. **Clone the repository:**

git clone https://github.com/cis-muzahid/django_ecommerce.git


2. **Navigate to the project directory:**

cd django_ecommerce

3. **Install dependencies:**

pip install -r requirements.txt

4. **Run migrations:**
   
python manage.py migrate

5. **Start the development server:**

python manage.py runserver


## Usage

- Access the main website at `http://localhost:8000/`
- Access the admin dashboard at `http://localhost:8000/admin/`

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


