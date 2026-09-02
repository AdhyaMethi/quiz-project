# URL patterns define karne ke liye Django ka path function import kar rahe hain
from django.urls import path

# Usi folder ke views.py module ko import kar rahe hain jisme saare view functions hain
from . import views


# ==============================================================================
# URL ROUTING TABLE (quiz/urls.py)
# ==============================================================================
# urlpatterns list mein browser ke URL aur views.py ke functions ki mapping hoti hai
urlpatterns = [
    # 1. Home Page Route:
    # URL: http://127.0.0.1:8000/
    # Yeh views.py ke home() function ko call karta hai
    # name='home' ka use hum template mein {% url 'home' %} likhne ke liye karte hain
    path('', views.home, name='home'),

    # 2. Quiz List Route:
    # URL: http://127.0.0.1:8000/quizzes/
    # Yeh views.py ke quiz_list() function ko call karta hai aur saari active quizzes dikhata hai
    path('quizzes/', views.quiz_list, name='quiz_list'),

    # 3. Quiz Detail Route (Dynamic Parameter):
    # URL: http://127.0.0.1:8000/quiz/1/
    # <int:quiz_id> URL se integer number capture karke views.quiz_detail(request, quiz_id) ko pass karta hai
    path('quiz/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),

    # 4. Quiz Submit Action Route:
    # URL: http://127.0.0.1:8000/quiz/1/submit/
    # Jab student form submit karta hai toh answers submit_quiz view ko bheje jaate hain
    path('quiz/<int:quiz_id>/submit/', views.submit_quiz, name='submit_quiz'),

    # 5. Result Page Route:
    # URL: http://127.0.0.1:8000/result/
    # Quiz submit hone ke baad final scorecard aur review answers yahan dikhte hain
    path('result/', views.result, name='result'),
]
