# Custom Django management command banane ke liye BaseCommand import kar rahe hain
from django.core.management.base import BaseCommand

# Database mein sample quiz aur questions save karne ke liye models import kar rahe hain
from quiz.models import Quiz, Question


# ==============================================================================
# CUSTOM MANAGEMENT COMMAND: python manage.py load_sample_data
# ==============================================================================
class Command(BaseCommand):
    # Terminal mein command ka description / help text
    help = 'Populates the database with sample quizzes and questions for testing.'

    # Jab bhi command execute hoti hai toh handle() function chalta hai
    def handle(self, *args, **options):
        # Terminal mein message print kar rahe hain
        self.stdout.write(self.style.NOTICE("Creating sample quiz data..."))

        # -------------------------------------------------------------
        # Sample Quiz 1: Python Basics
        # -------------------------------------------------------------
        # get_or_create check karta hai: agar "Python Basics" quiz pehle se hai toh use utha lo, nahi toh nayi bana do
        quiz_python, created = Quiz.objects.get_or_create(
            title="Python Basics",
            defaults={
                'description': (
                    "Test your fundamental understanding of Python programming, "
                    "including syntax, data types, functions, and key principles."
                ),
                'is_active': True,
            }
        )

        # Agar nayi quiz bani hai
        if created:
            self.stdout.write(self.style.SUCCESS(f"Created Quiz: '{quiz_python.title}'"))
        else:
            self.stdout.write(self.style.WARNING(f"Quiz '{quiz_python.title}' already exists. Updating questions..."))

        # Pehle ke purane duplicate sawal delete kar rahe hain taki clean data rahe
        quiz_python.questions.all().delete()

        # Python Basics ke liye 6 high-quality questions ki list
        python_questions = [
            {
                'question_text': "What is the correct file extension for Python files?",
                'option1': ".pyth",
                'option2': ".pt",
                'option3': ".py",
                'option4': ".pyt",
                'correct_answer': "option3", # Sahi jawab .py hai
            },
            {
                'question_text': "Which keyword is used to define a function in Python?",
                'option1': "def",
                'option2': "function",
                'option3': "fun",
                'option4': "define",
                'correct_answer': "option1", # Sahi jawab def hai
            },
            {
                'question_text': "Which built-in Python data structure is immutable?",
                'option1': "List",
                'option2': "Tuple",
                'option3': "Dictionary",
                'option4': "Set",
                'correct_answer': "option2", # Sahi jawab Tuple hai
            },
            {
                'question_text': "What is the output of type(3.14) in Python?",
                'option1': "<class 'int'>",
                'option2': "<class 'double'>",
                'option3': "<class 'number'>",
                'option4': "<class 'float'>",
                'correct_answer': "option4", # Sahi jawab float hai
            },
            {
                'question_text': "Which character is used for single-line comments in Python?",
                'option1': "//",
                'option2': "/*",
                'option3': "#",
                'option4': "--",
                'correct_answer': "option3", # Sahi jawab # hai
            },
            {
                'question_text': "What is the correct way to create a dictionary in Python?",
                'option1': "d = [\"name\": \"Alice\"]",
                'option2': "d = {\"name\": \"Alice\"}",
                'option3': "d = (\"name\": \"Alice\")",
                'option4': "d = <\"name\": \"Alice\">",
                'correct_answer': "option2", # Sahi jawab {key: value} curly braces hai
            },
        ]

        # Loop chala kar har ek question ko database mein create kar rahe hain
        for q_data in python_questions:
            # Question table mein naya row insert ho raha hai
            Question.objects.create(quiz=quiz_python, **q_data)

        # Success message print kar rahe hain
        self.stdout.write(self.style.SUCCESS(f"Added {len(python_questions)} questions to '{quiz_python.title}'"))

        # -------------------------------------------------------------
        # Sample Quiz 2: Django Fundamentals
        # -------------------------------------------------------------
        # Doosri quiz banate hain: Django Fundamentals
        quiz_django, created = Quiz.objects.get_or_create(
            title="Django Fundamentals",
            defaults={
                'description': (
                    "Assess your knowledge of Django MTV architecture, ORM, "
                    "templates, URL routing, and administration."
                ),
                'is_active': True,
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f"Created Quiz: '{quiz_django.title}'"))
        else:
            self.stdout.write(self.style.WARNING(f"Quiz '{quiz_django.title}' already exists. Updating questions..."))

        # Purane sawal clean kar rahe hain
        quiz_django.questions.all().delete()

        # Django Fundamentals ke 5 sawal
        django_questions = [
            {
                'question_text': "Which architectural pattern does Django closely follow?",
                'option1': "Model-Template-View (MVT)",
                'option2': "Flux Pattern",
                'option3': "Event Sourcing",
                'option4': "Microkernel",
                'correct_answer': "option1", # Sahi jawab MVT hai
            },
            {
                'question_text': "Which command is used to apply database migrations in Django?",
                'option1': "python manage.py runserver",
                'option2': "python manage.py makemigrations",
                'option3': "python manage.py migrate",
                'option4': "python manage.py startapp",
                'correct_answer': "option3", # Sahi jawab migrate hai
            },
            {
                'question_text': "Which security tag must be included inside POST forms in Django templates?",
                'option1': "{% secure_form %}",
                'option2': "{% csrf_token %}",
                'option3': "{% auth_token %}",
                'option4': "{% verify_post %}",
                'correct_answer': "option2", # Sahi jawab csrf_token hai
            },
            {
                'question_text': "In which file do you register models to make them visible in Django Admin?",
                'option1': "models.py",
                'option2': "views.py",
                'option3': "admin.py",
                'option4': "apps.py",
                'correct_answer': "option3", # Sahi jawab admin.py hai
            },
            {
                'question_text': "What is the primary role of urls.py in a Django application?",
                'option1': "To design CSS stylesheets",
                'option2': "To route incoming HTTP requests to corresponding view functions",
                'option3': "To manage database tables and migrations",
                'option4': "To store session cookies",
                'correct_answer': "option2", # Sahi jawab routing requests hai
            },
        ]

        # Django questions ko database mein save kar rahe hain
        for q_data in django_questions:
            Question.objects.create(quiz=quiz_django, **q_data)

        # Output feedback
        self.stdout.write(self.style.SUCCESS(f"Added {len(django_questions)} questions to '{quiz_django.title}'"))
        self.stdout.write(self.style.SUCCESS("\nSample data successfully loaded!"))
