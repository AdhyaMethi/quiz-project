"""
Root URL Configuration for quiz_project.
Yeh poore Django project ka main router hai jahan se requests alag-alag apps ko bheji jaati hain.
"""

# Django Admin panel ke URLs import kar rahe hain
from django.contrib import admin

# path routing ke liye aur include doosre apps ke urls.py ko jodane ke liye import kar rahe hain
from django.urls import path, include


# ==============================================================================
# MAIN PROJECT URL ROUTING
# ==============================================================================
urlpatterns = [
    # 1. Admin Portal URL:
    # Browser mein http://127.0.0.1:8000/admin/ kholne par Django ka built-in Admin dashboard open hota hai
    path('admin/', admin.site.urls),

    # 2. Quiz App URLs:
    # Baaki sabhi requests ('') ko seedha 'quiz.urls' file ki taraf forward (include) kar diya gaya hai
    path('', include('quiz.urls')),
]
