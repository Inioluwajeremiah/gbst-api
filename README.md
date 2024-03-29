# gbst-api

The GBST Flask application is a AI based application built to serve various functionalities related to healthcare and pregnancy monitoring. It provides endpoints for predicting GDM in pregnant women, managing medical records, user profiles, and notifications.

## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Configuration](#configuration)
- [Endpoints](#endpoints)
  - [Home](#home)
  - [Blood Sugar Test](#blood-sugar-test)
  - [Childbirth Outcome](#childbirth-outcome)
  - [Clinical History](#clinical-history)
  - [Diet](#diet)
  - [Enrollment](#enrollment)
  - [Exercise](#exercise)
  - [Fetal Kick Count](#fetal-kick-count)
  - [Medical History](#medical-history)
  - [Obstetric Information](#obstetric-information)
  - [Prediction](#prediction)
  - [Profile](#profile)
  - [User Registration](#user-registration)
  - [User Sign-In](#user-sign-in)
  - [User Sign-Out](#user-sign-out)
  - [Email Verification](#email-verification)
  - [Notifications](#notifications)

## Getting Started

### Prerequisites

- Python 3.x
- Flask
- Flask SQLAlchemy
- Flask Migrate
- Flask CORS
- Flask Mail
- Flask Login

### Installation

1. Clone the GBST Flask Application repository from [GitHub](https://github.com/your-github-repo-link).

2. Install the required Python packages:

   ```bash
   pip install flask flask_sqlalchemy flask_migrate flask_cors flask_mail flask_login
   ```

3. Set up your database and configure it in the `config.py` file.

4. Run the application:

   ```bash
   python run.py
   ```

## Configuration

The application uses a configuration file (`config.py`) to store various settings, including database configurations, API keys, and more. Make sure to configure this file according to your requirements.

## Endpoints

### Home

- **Endpoint**: `/`
- **Description**: Home endpoint, returns a welcome message.
- **HTTP Method**: GET

### Blood Sugar Test

- **Endpoint**: `/blood_sugar_test`
- **Description**: Endpoint for managing blood sugar test records.
- **HTTP Methods**: GET, POST

### Childbirth Outcome

- **Endpoint**: `/child_birth_outcome`
- **Description**: Endpoint for managing childbirth outcome records.
- **HTTP Methods**: GET, POST

### Clinical History

- **Endpoint**: `/clinical_history`
- **Description**: Endpoint for managing clinical history records.
- **HTTP Methods**: GET, POST

### Diet

- **Endpoint**: `/diet`
- **Description**: Endpoint for managing diet records.
- **HTTP Methods**: GET, POST

### Enrollment

- **Endpoint**: `/enrollment`
- **Description**: Endpoint for managing enrollment records.
- **HTTP Methods**: GET, POST

### Exercise

- **Endpoint**: `/exercise`
- **Description**: Endpoint for managing exercise records.
- **HTTP Methods**: GET, POST

### Fetal Kick Count

- **Endpoint**: `/fetal_kick_count`
- **Description**: Endpoint for managing fetal kick count records.
- **HTTP Methods**: GET, POST

### Medical History

- **Endpoint**: `/medical_history`
- **Description**: Endpoint for managing medical history records.
- **HTTP Methods**: GET, POST

### Obstetric Information

- **Endpoint**: `/obstetric_information`
- **Description**: Endpoint for managing obstetric information records.
- **HTTP Methods**: GET, POST

### Prediction

- **Endpoint**: `/predict`
- **Description**: Endpoint for making predictions based on medical data.
- **HTTP Method**: POST

### Profile

- **Endpoint**: `/profile`
- **Description**: Endpoint for managing user profiles.
- **HTTP Methods**: GET, PUT

### User Registration

- **Endpoint**: `/signup`
- **Description**: Endpoint for user registration.
- **HTTP Method**: POST

### User Sign-In

- **Endpoint**: `/signin`
- **Description**: Endpoint for user sign-in.
- **HTTP Method**: POST

### User Sign-Out

- **Endpoint**: `/signout`
- **Description**: Endpoint for user sign-out.
- **HTTP Method**: POST

### Email Verification

- **Endpoint**: `/verify`
- **Description**: Endpoint for email verification.
- **HTTP Method**: POST

### Notifications

- **Endpoint**: `/notification`
- **Description**: Endpoint for managing notifications.
- **HTTP Methods**: GET, POST

