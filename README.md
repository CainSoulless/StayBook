# REFFBOOK

**REFFBOOK** is a web application developed in Django for managing hotel room reservations. This project allows users to browse available rooms, make reservations, and view booking histories, with functionalities supported by Django's robust backend framework.

## Features

- User authentication and profile management (Admin and Client roles)
- Room reservation system
- Reservation history tracking
- Integration with payment methods for bookings
- Responsive design with Bootstrap
- Simple and intuitive user interface

## Tech Stack

- **Backend**: Django 5.1.1
- **Frontend**: HTML, CSS (Bootstrap 5), JavaScript
- **Database**: SQLite (default, can be changed to PostgreSQL for production)
- **Deployment**: Heroku

## Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/CainSoulless/REFFBOOK.git
    ```

2. Navigate to the project directory:
    ```bash
    cd REFFBOOK
    ```

3. Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate   # For Mac/Linux
    venv\Scripts\activate      # For Windows
    ```

4. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

5. Apply migrations:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

6. Run the local development server:
    ```bash
    python manage.py runserver
    ```

Visit `http://127.0.0.1:8000/` in your web browser to use the app locally.

## Usage

- **Admin**: Administrators can add rooms, manage reservations, and view clients' data.
- **Client**: Clients can browse rooms, make reservations, and manage their booking history.

## Deployment

REFFBOOK is deployed using **Heroku**. For instructions on deploying to Heroku, ensure you have the necessary environment variables set up and a PostgreSQL database configured.

1. Log in to Heroku:
    ```bash
    heroku login
    ```

2. Create a new Heroku app:
    ```bash
    heroku create
    ```

3. Deploy the application:
    ```bash
    git push heroku main
    ```

4. Set up the database on Heroku:
    ```bash
    heroku run python manage.py migrate
    ```

## Contributing

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

### Contact

For questions or support, please contact [CainSoulless](https://github.com/CainSoulless).
