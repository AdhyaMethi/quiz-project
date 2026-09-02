# Django ka forms module import kar rahe hain ModelForm banane ke liye
from django import forms

# Hamare models import kar rahe hain
from .models import Quiz, Question


# ==============================================================================
# 1. QUIZ MODEL FORM
# ==============================================================================
# Yeh form Quiz model par based HTML form generate karne ke liye use hota hai
class QuizForm(forms.ModelForm):
    # Meta class form ko model aur fields ke sath map karti hai
    class Meta:
        # Yeh form Quiz model ke data ke sath judega
        model = Quiz

        # Form mein kaun-kaun se fields dikhane hain
        fields = ['title', 'description', 'is_active']

        # HTML input elements ke CSS classes aur placeholders customize karne ke liye widgets
        widgets = {
            # Title input box ke liye class aur placeholder
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Python Fundamentals'}),
            # Description textarea ke liye rows, class aur placeholder
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4, 'placeholder': 'Describe what topics this quiz covers...'}),
            # is_active checkbox ke liye CSS class
            'is_active': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }


# ==============================================================================
# 2. QUESTION MODEL FORM
# ==============================================================================
# Yeh form Question model par based form generate karne ke liye use hota hai
class QuestionForm(forms.ModelForm):
    class Meta:
        # Yeh form Question model ke data ke sath judega
        model = Question

        # Question form mein dikhne wale fields
        fields = ['quiz', 'question_text', 'option1', 'option2', 'option3', 'option4', 'correct_answer']

        # Inputs ko styling dene ke liye widgets
        widgets = {
            'quiz': forms.Select(attrs={'class': 'form-select'}),
            'question_text': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3, 'placeholder': 'Enter question here...'}),
            'option1': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Option 1'}),
            'option2': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Option 2'}),
            'option3': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Option 3'}),
            'option4': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Option 4'}),
            'correct_answer': forms.Select(attrs={'class': 'form-select'}),
        }
