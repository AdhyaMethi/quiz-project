# ⚡ QuizMaster - Django Quiz Application

A beginner-friendly, full-featured **Quiz Application** built with **Python, Django, MySQL, HTML, CSS, and JavaScript**.

This project provides a complete end-to-end interactive experience:
- **Students** can browse quizzes, answer multiple-choice questions with a live timer, submit answers, and receive instant score breakdowns and percentage calculations.
- **Teachers / Administrators** can manage quizzes and questions using the built-in Django Admin interface.

---

## 📋 Table of Contents

1. [Features](#-features)
2. [Technologies Used](#-technologies-used)
3. [Project Folder Structure](#-project-folder-structure)
4. [Step-by-Step Setup Guide](#-step-by-step-setup-guide)
   - [Step 1: Prerequisites](#step-1-prerequisites)
   - [Step 2: Create & Activate Virtual Environment](#step-2-create--activate-virtual-environment)
   - [Step 3: Install Required Packages](#step-3-install-required-packages)
   - [Step 4: MySQL Database Setup](#step-4-mysql-database-setup)
   - [Step 5: Configure Database Credentials](#step-5-configure-database-credentials)
   - [Step 6: Run Database Migrations](#step-6-run-database-migrations)
   - [Step 7: Create Superuser (Admin Account)](#step-7-create-superuser-admin-account)
   - [Step 8: Load Sample Quiz Data](#step-8-load-sample-quiz-data)
   - [Step 9: Run the Development Server](#step-9-run-the-development-server)
5. [Teacher / Admin Guide](#-teacher--admin-guide)
6. [Student Workflow](#-student-workflow)
7. [Running Automated Tests](#-running-automated-tests)
8. [Common Errors & Solutions (Troubleshooting)](#-common-errors--solutions-troubleshooting)

---

## 🚀 Features

- **Interactive Quizzes**: Multiple-choice format with 4 options per question.
- **Instant Backend Evaluation**: Secure server-side score calculation; answers cannot be manipulated via frontend.
- **Detailed Result Dashboard**: Displays Total Questions, Correct Answers, Wrong Answers, Percentage, and a full question-by-question review.
- **Responsive & Modern UI**: Built with pure CSS (no bloated UI frameworks needed). Mobile-friendly and clean.
- **Django Admin Integration**: Custom admin models with inline editing, search, and filtering by quiz.
- **Safety Checks**: Handles inactive quizzes, empty quizzes, direct URL access, and unselected options gracefully.
- **Pre-submission Confirmation**: Alerts student if any questions are left unanswered before submitting.

---

## 🛠️ Technologies Used

- **Backend**: Python 3.10+, Django (4.2+)
- **Database**: MySQL (using Django ORM and PyMySQL/mysqlclient)
- **Frontend**: HTML5, CSS3, JavaScript (ES6)
- **Architecture**: Model-Template-View (MTV) / Function-Based Views (FBVs)

---

## 📁 Project Folder Structure

```text
quiz_application/
├── manage.py                   # Django CLI entrypoint
├── requirements.txt            # Python dependencies
├── README.md                   # Complete documentation
│
├── quiz_project/               # Main Project Configuration
│   ├── __init__.py             # PyMySQL compatibility hook
│   ├── settings.py             # App, database, and template settings
│   ├── urls.py                 # Root URL router
│   ├── asgi.py                 # ASGI configuration
│   └── wsgi.py                 # WSGI configuration
│
├── quiz/                       # Quiz Application Core
│   ├── __init__.py
│   ├── admin.py                # Admin portal configurations & inlines
│   ├── apps.py                 # App configuration
│   ├── forms.py                # Model forms reference
│   ├── models.py               # Quiz & Question models
│   ├── tests.py                # Unit and integration tests
│   ├── urls.py                 # Quiz route definitions
│   ├── views.py                # Beginner-friendly function-based views
│   └── management/
│       └── commands/
│           └── load_sample_data.py  # Sample quiz data generator
│
├── templates/                  # HTML Templates (Django Template Engine)
│   ├── base.html               # Base layout with navbar and footer
│   ├── home.html               # Welcome landing page & highlights
│   ├── quiz_list.html          # Quiz catalogue grid
│   ├── quiz_detail.html        # Question list with radio choices & timer
│   └── result.html             # Result scorecard and review breakdown
│
└── static/                     # Static Assets
    ├── css/
    │   └── style.css           # Modern custom stylesheet
    └── js/
        └── script.js           # Client-side validation, timer, and highlights
```

---

## 💻 Step-by-Step Setup Guide

Follow these steps in your terminal (PowerShell, Command Prompt, or VS Code Terminal).

### Step 1: Prerequisites

Make sure Python is installed on your computer:
```powershell
python --version
```
*(If Python is not recognized, install Python 3.10+ and check the "Add Python to PATH" box during installation).*

---

### Step 2: Create & Activate Virtual Environment

Open your terminal in the `quiz_application` directory:

```powershell
# Navigate into the project folder
cd quiz_application

# Create a virtual environment named 'venv'
python -m venv venv

# Activate virtual environment on Windows (PowerShell or CMD)
venv\Scripts\activate
```

> **Note**: When activated, you will see `(venv)` at the beginning of your terminal prompt.

---

### Step 3: Install Required Packages

Install Django and the database connectors:

```powershell
pip install -r requirements.txt
```

---

### Step 4: MySQL Database Setup

1. Open your MySQL client (e.g., MySQL Workbench, XAMPP phpMyAdmin, or MySQL Command Line).
2. Create a new database named `quiz_db`:

```sql
CREATE DATABASE quiz_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

---

### Step 5: Configure Database Credentials

Open `quiz_project/settings.py` in VS Code and locate the `DATABASES` setting:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'quiz_db',
        'USER': 'root',
        'PASSWORD': 'your_password',  # ⚠️ Replace with your actual MySQL password
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

> 💡 **Quick SQLite Tip for Testing**: If you don't have MySQL installed on your local machine yet, you can temporarily set the environment variable `$env:USE_SQLITE="True"` or toggle `USE_SQLITE_FALLBACK = True` in `settings.py` to test with SQLite!

---

### Step 6: Run Database Migrations

Migrations create the necessary tables in your database (for Django auth, sessions, quizzes, and questions).

```powershell
# 1. Create migration files based on our models
python manage.py makemigrations

# 2. Apply migrations to the database
python manage.py migrate
```

**What do these commands do?**
- `makemigrations`: Inspects `quiz/models.py` and prepares SQL migration instructions.
- `migrate`: Executes the SQL instructions to create and update tables in MySQL.

---

### Step 7: Create Superuser (Admin Account)

Create an administrator account to access the Django Admin portal:

```powershell
python manage.py createsuperuser
```

Follow the interactive prompts:
- **Username**: `admin`
- **Email**: `admin@example.com` (or press Enter to skip)
- **Password**: *(enter a secure password, e.g. `admin123`)*

---

### Step 8: Load Sample Quiz Data

We have provided a built-in helper command to populate sample quizzes (e.g., "Python Basics" and "Django Fundamentals") with questions:

```powershell
python manage.py load_sample_data
```

You should see:
```text
Creating sample quiz data...
Created Quiz: 'Python Basics'
Added 6 questions to 'Python Basics'
Created Quiz: 'Django Fundamentals'
Added 5 questions to 'Django Fundamentals'
Sample data successfully loaded!
```

---

### Step 9: Run the Development Server

Start the local Django web server:

```powershell
python manage.py runserver
```

Open your browser and visit:
- **Student Home Page**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Quiz Catalog**: [http://127.0.0.1:8000/quizzes/](http://127.0.0.1:8000/quizzes/)
- **Django Admin Portal**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 👩‍🏫 Teacher / Admin Guide

### How to Add & Manage Quizzes

1. Go to [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) and log in with your superuser credentials.
2. Under **Quiz Application**:
   - Click **Quizzes** to add a new quiz (Enter Title, Description, and check Active).
   - You can add questions directly inside the quiz page using the inline editor at the bottom!
   - Alternatively, click **Questions** to add/edit individual questions with four options and choose the correct answer choice.
3. You can search questions by text or filter by quiz topic.

---

## 🧑‍🎓 Student Workflow

1. Open the homepage: `http://127.0.0.1:8000/`
2. Click **View Quizzes** to view all active quizzes.
3. Select any quiz and click **Start Quiz**.
4. Read each question and click your desired answer option.
5. Click **Submit Quiz Answers**. A confirmation popup will alert you if any questions were missed.
6. View your score, percentage, and detailed answers on the **Result Page**.
7. Click **Try Again** or **Back to Quizzes** to take another quiz.

---

## 🧪 Running Automated Tests

Run the included automated unit test suite to verify models, views, and score calculations:

```powershell
python manage.py test quiz
```

Expected output:
```text
Found 8 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
........
----------------------------------------------------------------------
Ran 8 tests in 0.050s

OK
```

---

## ⚠️ Common Errors & Solutions (Troubleshooting)

### 1. `django.db.utils.OperationalError: (2003, "Can't connect to MySQL server")`
- **Cause**: MySQL server is not running or the port is incorrect.
- **Fix**: Start MySQL service via MySQL Workbench / XAMPP Control Panel / Windows Services.

### 2. `django.db.utils.OperationalError: (1049, "Unknown database 'quiz_db'")`
- **Cause**: The database `quiz_db` does not exist yet.
- **Fix**: Run `CREATE DATABASE quiz_db;` in your MySQL console.

### 3. `django.db.utils.OperationalError: (1045, "Access denied for user 'root'@'localhost'")`
- **Cause**: Incorrect MySQL password in `settings.py`.
- **Fix**: Update `'PASSWORD': 'your_actual_password'` in `quiz_project/settings.py`.

### 4. `No module named 'pymysql'`
- **Fix**: Run `pip install pymysql` inside your activated virtual environment.

### 5. `Execution of scripts is disabled on this system` (PowerShell)
- **Fix**: Run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in PowerShell, then run `venv\Scripts\activate`.

---

## 🎓 Summary of Views & URLs

| URL Pattern | View Name | Description |
| :--- | :--- | :--- |
| `/` | `home` | Landing page with overview and stats |
| `/quizzes/` | `quiz_list` | Shows all published quizzes |
| `/quiz/<id>/` | `quiz_detail` | Displays questions and 4 options |
| `/quiz/<id>/submit/` | `submit_quiz` | Evaluates answers & saves result in session |
| `/result/` | `result` | Displays final score, percentage & review |
| `/admin/` | `admin.site.urls` | Teacher portal for managing quizzes |

---

*Happy Coding & Learning! 🚀*
