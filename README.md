# React + Django Login Project

This project contains a **React frontend** and a **Django backend** for a simple login system.

---

## Project Structure

```
Login-project
│
├── backend
│   ├── manage.py
│   ├── backend
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── ...
│   └── users
│       ├── views.py
│       └── ...
│
└── frontend
    ├── public
    ├── src
    └── package.json
```

---

# Prerequisites

Install these tools before running the project:

* Python (3.10 or higher)
* Node.js and npm
* Git (optional)

---

# Backend Setup (Django)

### 1. Go to backend folder

```
cd backend
```

### 2. Create virtual environment

```
python -m venv .venv
```

### 3. Activate virtual environment

Windows:

```
.venv\Scripts\activate
```

Mac/Linux:

```
source .venv/bin/activate
```

### 4. Install dependencies

```
pip install django djangorestframework django-cors-headers
```

### 5. Apply migrations

```
python manage.py migrate
```

### 6. Run backend server

```
python manage.py runserver
```

Backend will start at:

```
http://127.0.0.1:8000
```

---

# Frontend Setup (React)

### 1. Go to frontend folder

```
cd frontend
```

### 2. Install dependencies

```
npm install
```

### 3. Start React server

```
npm start
```

Frontend will start at:

```
http://localhost:3000
```

---

# How the Project Works

1. User enters **email and password** on the React login page.
2. React sends a **POST request** to the Django API.
3. Django checks the credentials.
4. Django sends a response back to React.
5. React shows **success or failure message**.

---

# Running the Project

Start both servers:

Backend:

```
cd backend
python manage.py runserver
```

Frontend:

```
cd frontend
npm start
```

Open browser:

```
http://localhost:3000
```

---

# Author

Login Project using **React + Django**
