# CivicWatch API

**CivicWatch API** is a public incident reporting system designed to bridge the gap between citizens and local authorities. It provides a simple, RESTful API that allows the public to report local issues like potholes, water leaks, or broken streetlights, and for administrators to track and resolve these reports.

---

### Core Features

* **Public Incident Reporting**: Anonymous and authenticated users can submit incident reports with details, location, and a photo.
* **Status Management**: Admins can review reports and update their status (`Pending`, `In Review`, `Resolved`, `Rejected`).
* **Auditable History**: Every status change is logged with comments and timestamps for full transparency.
* **Role-Based Access**: The system distinguishes between regular `citizen` users and `admin` users with special privileges. 
* **JWT Authentication**: Secure, token-based authentication for user-specific actions. 
* **Analytics Dashboard**: An admin-only endpoint provides summary statistics of all incidents. 

---

### Tech Stack

* **Backend**: Python, Django, Django REST Framework 
* **Database**: PostgreSQL for production, SQLite for development 
* **Authentication**: SimpleJWT for token-based authentication 
* **Image Handling**: Cloudinary for cloud-based image uploads and storage 
* **Deployment**: Render 
* **API Documentation**: Swagger/OpenAPI via `drf-yasg` 

---

### API Endpoints

The base URL is `/api/`.

#### Authentication (`/api/users/`)

| Method | Endpoint             | Permission    | Description                                       |
| :----- | :------------------- | :------------ | :------------------------------------------------ |
| `POST` | `/register/`         | **Public** | Register a new user with a username and password. |
| `POST` | `/login/`       | **Public** | Log in to receive JWT access and refresh tokens.  |
| `POST` | `/jwt/refresh/`      | **Public** | Obtain a new access token using a refresh token.  |
| `GET`  | `/profile/`               | Authenticated | Get the profile of the currently logged-in user.  |

#### Incidents (`/api/incidents/`)

| Method | Endpoint             | Permission    | Description                                       |
| :----- | :------------------- | :------------ | :------------------------------------------------ |
| `POST` | `/`                  | **Public** | Submit a new incident report. Anonymous allowed.  |
| `GET`  | `/`                  | **Public** | List all incidents. Supports filtering and sorting. |
| `GET`  | `/{id}/`             | **Public** | Retrieve the details of a single incident.        |
| `PUT`  | `/{id}/status/`      | **Admin Only**| Update the status of an incident.                 |
| `GET`  | `/{id}/history/`     | **Admin Only**| View the status change history for an incident.   |

#### Analytics (`/api/analytics/`)

| Method | Endpoint             | Permission    | Description                                       |
| :----- | :------------------- | :------------ | :------------------------------------------------ |
| `GET`  | `/dashboard/`        | **Admin Only**| Get summary stats (counts by status, category, etc).|


---

### Local Setup and Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/Blackburn0/CivicWatch.git
    cd civicwatch
    ```

2.  **Create and Activate Virtual Environment**
    ```bash
    # Mac/Linux
    python3 -m venv venv
    source venv/bin/activate

    # Windows
    python -m venv venv
    venv\Scripts\activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set Up Environment Variables**
    -   Create a `.env` file in the project root by copying the example: `cp .env.example .env`.
    -   Fill in the required values like `SECRET_KEY` and `CLOUDINARY_URL`. For local development, the `DATABASE_URL` can remain `sqlite:///db.sqlite3`. 

5.  **Run Database Migrations**
    ```bash
    python manage.py migrate
    ```

6.  **Create a Superuser (Admin)**
    ```bash
    python manage.py createsuperuser
    ```

7.  **Run the Development Server**
    ```bash
    python manage.py runserver
    ```
    The API will be available at `http://127.0.0.1:8000`.

---

### Interactive API Documentation

This project uses `drf-yasg` to provide a Swagger UI for interactive API documentation. Once the server is running, you can access it at:

* **Swagger UI**: `http://127.0.0.1:8000/swagger/`
* **ReDoc**: `http://127.0.0.1:8000/redoc/`