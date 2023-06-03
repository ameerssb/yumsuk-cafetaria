Yumsuk Cafeteria is an open-source web application that enables users to conveniently order food from their preferred cafeteria. The project aims to provide a seamless and user-friendly experience for both customers and cafeteria owners, streamlining the food ordering process.

Features:

User Registration and Authentication:
Users can create new accounts or log in using existing credentials.
User authentication is implemented to ensure secure access to personal information.

Cafeteria Selection:
Users can browse and choose from a list of available cafeterias.
Cafeteria details, including location, menu, and operating hours, are displayed.

Menu Display and Customization:
The application displays the cafeteria's menu with detailed information about each dish, including descriptions and prices.
Users can customize their orders by selecting specific ingredients, requesting modifications, or adding additional items.

Cart Management:
Users can add items to their cart, view a summary of their order, and make changes as needed.
Quantity adjustments, item removal, and price calculation are implemented for a smooth ordering experience.

Order Placement and Payment:
Users can securely place their orders, select a preferred payment method, and provide delivery or pickup details.
Multiple payment options, such as credit cards, digital wallets, and online banking, are supported.

Order Tracking and History:
Users can track the status of their orders in real-time, from preparation to delivery.
Order history is stored, allowing users to easily reorder their favorite meals or view past transactions.

Admin Panel:
Cafeteria owners or administrators have access to an admin panel for managing menus, updating availability, and monitoring orders.
They can add new dishes, modify prices, adjust operating hours, and receive notifications about new orders.

Feedback and Support:
The application provides a feedback mechanism for users to share their experiences and suggestions.
Users can contact customer support for assistance or report any issues they encounter.
Technologies Used:

Front-end: HTML, CSS, JavaScript
Back-end: Python, Django Framework
Database: Mysql
Payment Integration: Paystack Api
User Authentication: Django Authentication

Installation:
Clone the repository to your local machine.
git clone https://github.com/ameerssb/yumsuk-cateria.git

Install the required dependencies:
cd yumsuk-cafeteria
pip install -r requirements.txt

Set up the database:
Create a new database using your preferred database management system (e.g., PostgreSQL, MySQL, SqLite3).

Update the database configuration in the settings.py file with your database details.

Run database migrations to create the necessary tables:
python manage.py migrate

Create a superuser for admin access:
python manage.py createsuperuser

Start the development server:
python manage.py runserver

Access the application:
Open a web browser and navigate to http://localhost:8000 (or the specified port if modified).
Login with the superuser account created in step 5.

License
This project is licensed under the MIT License. Feel free to use and modify the system as per your requirements.

Contributing:
Contributions to Yumsuk Cafeteria are welcome! Whether you're a developer, designer, or tester, you can contribute by submitting bug reports, feature requests, or pull requests. Please refer to the project's documentation and guidelines for contributing.
