"""
Django settings for quiz_project.
Is file mein project ki saari main configurations aur settings hoti hain.
"""

# File paths ko manage karne ke liye Python ka built-in pathlib module import kar rahe hain
from pathlib import Path
# Environment variables (jaise passwords aur keys) read karne ke liye os module import kar rahe hain
import os

# .env file se secret passwords aur database settings load karne ki koshish kar rahe hain
try:
    # python-dotenv library se load_dotenv function import kar rahe hain
    from dotenv import load_dotenv
    # BASE_DIR project ke root folder (quiz_application) ka absolute path nikalta hai
    BASE_DIR = Path(__file__).resolve().parent.parent
    # .env file ko load karke environment variables mein inject kar rahe hain
    load_dotenv(BASE_DIR / '.env')
except ImportError:
    # Agar dotenv package installed nahi hai, toh seedha path set kar rahe hain
    BASE_DIR = Path(__file__).resolve().parent.parent


# ==============================================================================
# SECURITY SETTINGS
# ==============================================================================

# SECRET_KEY Django mein sessions, cookies aur cryptographic signing ke liye use hota hai
# Environment variable se secret key padhi jaati hai, agar nahi mile toh fallback default use hoga
SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY', 
    'django-insecure-beginner-friendly-quiz-app-secret-key-2026'
)

# DEBUG=True ka matlab development mode ON hai (Errors terminal aur browser mein detail mein dikhenge)
# Production (live website) par ise hamesha False rakhna chahiye
DEBUG = True

# Kaunse domains/IP addresses is project ko access kar sakte hain ('*' ka matlab abhi sabhi allowed hain)
ALLOWED_HOSTS = ['*']


# ==============================================================================
# INSTALLED APPS CONFIGURATION
# ==============================================================================
# Yahan Django ko batate hain ki hamare project mein kaun-kaun se apps use ho rahe hain
INSTALLED_APPS = [
    # 1. Django ka built-in Admin Panel app
    'django.contrib.admin',
    # 2. User Authentication (login, logout, permissions, superuser) system
    'django.contrib.auth',
    # 3. Django Content Types framework (models ko track karne ke liye)
    'django.contrib.contenttypes',
    # 4. User Sessions manage karne ke liye (Quiz result session mein rakhne ke liye)
    'django.contrib.sessions',
    # 5. Flash Messages (Alerts) dikhane ke liye (jaise Success, Warning messages)
    'django.contrib.messages',
    # 6. CSS, JavaScript aur Images (Static Files) handle karne ke liye
    'django.contrib.staticfiles',

    # 7. Hamara khud ka banaya hua Quiz App
    'quiz.apps.QuizConfig',
]


# ==============================================================================
# MIDDLEWARE CONFIGURATION
# ==============================================================================
# Request aane aur Response jaane ke beech mein execute hone wale security filters
MIDDLEWARE = [
    # Basic security headers add karta hai
    'django.middleware.security.SecurityMiddleware',
    # Har user ke liye unique session maintain karta hai (results store karne ke liye zaroori)
    'django.contrib.sessions.middleware.SessionMiddleware',
    # Standard URL handling aur redirection rules provide karta hai
    'django.middleware.common.CommonMiddleware',
    # Cross-Site Request Forgery (CSRF) attacks se forms ko bachata hai
    'django.middleware.csrf.CsrfViewMiddleware',
    # Request ke sath logged-in user ki details (request.user) attach karta hai
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # Views se template mein temporary messages pass karta hai
    'django.contrib.messages.middleware.MessageMiddleware',
    # Clickjacking attacks se protect karta hai (website ko unauthorized iframes mein load hone se rokta hai)
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Root URL configuration file ka path (Routing yahan se shuru hoti hai)
ROOT_URLCONF = 'quiz_project.urls'


# ==============================================================================
# TEMPLATES CONFIGURATION
# ==============================================================================
# HTML templates ko render karne ki settings
TEMPLATES = [
    {
        # Django ka standard template engine use kar rahe hain
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Django ko bata rahe hain ki 'templates' folder project ke root par hai
        'DIRS': [BASE_DIR / 'templates'],
        # Apps ke andar bane template folders ko bhi automatically search karega
        'APP_DIRS': True,
        'OPTIONS': {
            # Har template mein automatically available hone wale context variables
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',       # request object ko template mein access karne ke liye
                'django.contrib.auth.context_processors.auth',      # user details access karne ke liye
                'django.contrib.messages.context_processors.messages', # flash messages access karne ke liye
            ],
        },
    },
]

# Web server ke liye WSGI application entrypoint
WSGI_APPLICATION = 'quiz_project.wsgi.application'


# ==============================================================================
# DATABASE CONFIGURATION (MySQL / SQLite Fallback)
# ==============================================================================
# USE_SQLITE flag check karte hain (Testing ke liye SQLite ya Live ke liye MySQL)
USE_SQLITE_FALLBACK = os.environ.get('USE_SQLITE', 'False').lower() in ('true', '1', 't')

if USE_SQLITE_FALLBACK:
    # Agar SQLite mode ON hai toh local db.sqlite3 file use hogi
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    # Default MySQL Database Configuration
    DATABASES = {
        'default': {
            # Django ka MySQL database engine backend
            'ENGINE': 'django.db.backends.mysql',
            # Database ka naam (jo aapne MySQL mein CREATE DATABASE quiz_db se banaya hai)
            'NAME': os.environ.get('MYSQL_DATABASE', 'quiz_db'),
            # MySQL server ka username (usually 'root')
            'USER': os.environ.get('MYSQL_USER', 'root'),
            # MySQL server ka password (apna password yahan ya .env file mein dalein)
            'PASSWORD': os.environ.get('MYSQL_PASSWORD', 'your_password'),
            # MySQL server host address (Local machine ke liye localhost)
            'HOST': os.environ.get('MYSQL_HOST', 'localhost'),
            # MySQL default port number (3306)
            'PORT': os.environ.get('MYSQL_PORT', '3306'),
            'OPTIONS': {
                # Strict SQL mode jisse invalid data save na ho sake
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
                # UTF-8 character encoding jisse emojis aur har language ka text support ho
                'charset': 'utf8mb4',
            }
        }
    }


# ==============================================================================
# PASSWORD VALIDATION
# ==============================================================================
# Admin password banate waqt security rules check karne ke liye
AUTH_PASSWORD_VALIDATORS = [
    # Password user ki personal details (naam, email) se milta-julta na ho
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    # Password kam se kam required length ka ho
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    # Aam aur common passwords (jaise 123456, password) ko block kare
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    # Poora password sirf numbers ka na ho
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ==============================================================================
# INTERNATIONALIZATION (LANGUAGE & TIMEZONE)
# ==============================================================================
# Default language code (English)
LANGUAGE_CODE = 'en-us'

# Timezone setting (UTC)
TIME_ZONE = 'UTC'

# Django translation system enable karein
USE_I18N = True

# Timezone-aware datetimes use karein
USE_TZ = True


# ==============================================================================
# STATIC FILES CONFIGURATION (CSS, JavaScript, Images)
# ==============================================================================
# Browser mein static files kis URL se access hongi (e.g. /static/css/style.css)
STATIC_URL = '/static/'

# Django ko static folder ka location batate hain
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Primary Key ke liye default field type (64-bit Big integer ID: 1, 2, 3...)
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
