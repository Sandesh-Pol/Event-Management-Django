# Event Tickets Management 🎟️

Welcome to the Event Tickets Management project! This application is built using Django and provides a platform for managing and purchasing event tickets. It features user authentication, email verification using OTP (One Time Password), and fully responsive web pages designed with cards.

## Features ✨

- **User Authentication**: Secure user login and registration.
- **Email Verification**: Verify users via email using OTP.
- **Responsive Design**: Fully responsive web pages with a modern card layout.
- **Event Management**: Create, view, and manage events.
- **Ticket Purchasing**: Simple and intuitive interface for purchasing tickets. (working on payment getway)

## Requirements 🛠️

To run this project, you'll need the following:

- Python 3.8+
- Django 3.2+
- Django Rest Framework
- Other dependencies as listed in `requirements.txt`

## Getting Started 🚀

Follow these steps to get the project up and running on your local machine.

### Clone the Repository

```bash
git clone https://github.com/your-username/event-tickets-management.git
cd event-tickets-management
```

### Set Up Virtual Environment

Create a virtual environment to install dependencies:

```bash
python -m venv env
source env/bin/activate   # On Windows use `env\Scripts\activate`
```

### Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### Database Migration

Apply database migrations:

```bash
python manage.py migrate
```

### Create a Superuser

Create a superuser to access the Django admin:

```bash
python manage.py createsuperuser
```

### Run the Server

Start the Django development server:

```bash
python manage.py runserver
```

### Access the Application

Open your web browser and go to:

```
http://127.0.0.1:8000/
```

You can now register, log in, and explore the Event Tickets Management system!

## How It Works 🧩

### User Authentication

- Users can register with their email and password.
- After registration, users receive an OTP via email to verify their account.

### Email Verification

- An OTP is sent to the user's email upon registration.
- Users need to enter the OTP to activate their account.

### Responsive Design

- The application uses a responsive design framework to ensure a seamless experience across devices.
- Cards are used extensively to display events and tickets, providing a clean and modern look.

## Contributing 🤝

We welcome contributions! Please read our [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests.

## License 📜

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact 📬

For any inquiries or feedback, please contact us at:

- Email: sandeshpol268@gmail.com


---

Thank you for using Event Tickets Management! We hope you find it helpful and easy to use. If you encounter any issues or have suggestions, please don't hesitate to reach out. 🌟

Happy Event Managing! 🎉
