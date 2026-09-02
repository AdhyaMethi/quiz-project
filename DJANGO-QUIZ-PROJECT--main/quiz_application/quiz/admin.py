# Django ka admin module import kar rahe hain jisse models ko admin panel mein register kar sakein
from django.contrib import admin

# Hamare models.py se Quiz aur Question models ko import kar rahe hain
from .models import Quiz, Question


# ==============================================================================
# 1. QUESTION INLINE CONFIGURATION
# ==============================================================================
# Yeh class Teacher/Admin ko suvidha deti hai ki Quiz banate waqt hi
# uske andar Questions bhi add/edit kar sakein (Alag se page par jane ki zaroorat nahi)
class QuestionInline(admin.StackedInline):
    # Kaunse model ke sawal inline dikhane hain
    model = Question

    # Nayi quiz banate waqt kitne khali question forms default mein dikhenge
    extra = 1

    # Questions box ko collapse (chupane/kholne) ki suvidha deta hai
    classes = ['collapse']


# ==============================================================================
# 2. QUIZ ADMIN CONFIGURATION
# ==============================================================================
# @admin.register(Quiz) decorator Quiz model ko Django admin panel mein register karta hai
@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    # Admin table mein kaun-kaun se columns dikhenge
    list_display = ('title', 'total_questions_display', 'is_active', 'created_at')

    # Right sidebar mein filter karne ke vikalp (Active/Inactive, Date)
    list_filter = ('is_active', 'created_at')

    # Admin table ke upar search bar deta hai (Quiz title ya description se search karne ke liye)
    search_fields = ('title', 'description')

    # List view mein hi bina page khole Active checkbox toggle karne ki suvidha
    list_editable = ('is_active',)

    # Upar banayi gayi QuestionInline class ko yahan attach kar diya
    inlines = [QuestionInline]

    # Custom column jo model ki total_questions property ko admin table mein dikhayega
    @admin.display(description='Total Questions')
    def total_questions_display(self, obj):
        # obj (Quiz) ke total questions ki count return karta hai
        return obj.total_questions


# ==============================================================================
# 3. QUESTION ADMIN CONFIGURATION
# ==============================================================================
# Question model ko admin panel mein register kar rahe hain
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    # Questions table mein dikhne wale columns
    list_display = ('question_text_summary', 'quiz', 'correct_answer', 'option1', 'option2')

    # Right sidebar mein filters: Quiz ke naam se aur Correct Answer se
    list_filter = ('quiz', 'correct_answer')

    # Search bar: Sawal ke text se ya uske options se search karne ke liye
    search_fields = ('question_text', 'quiz__title', 'option1', 'option2', 'option3', 'option4')

    # Bada question text table mein poora na dikh kar shuru ke 70 characters dikhe
    @admin.display(description='Question Text')
    def question_text_summary(self, obj):
        # 70 characters se lamba hone par aage '...' laga deta hai
        return obj.question_text[:70] + ('...' if len(obj.question_text) > 70 else '')
