# Django ke database models module ko import kar rahe hain jisse hum tables define kar sakein
from django.db import models


# ==============================================================================
# 1. QUIZ MODEL (Table: quiz_quiz)
# ==============================================================================
# Yeh class database mein Quiz naam ki ek table banayegi jisme quiz ki details store hongi
class Quiz(models.Model):
    # Quiz ka naam/title store karne ke liye (Jaise: Python Basics, Django Fundamentals)
    title = models.CharField(
        # max_length=200 ka matlab title maximum 200 characters lamba ho sakta hai
        max_length=200, 
        # help_text admin panel mein form bharte waqt hint ke roop mein dikhta hai
        help_text="Title of the quiz (e.g. Python Basics, Django Fundamentals)"
    )

    # Quiz ke baare mein vishrit jankari (description) store karne ke liye lamba text field
    description = models.TextField(
        help_text="Brief description explaining what this quiz covers"
    )

    # Quiz kis tareekh aur samay par banayi gayi thi, yeh auto_now_add se apne aap set ho jayega
    created_at = models.DateTimeField(
        # auto_now_add=True ka matlab record bante hi current timestamp save ho jayegi
        auto_now_add=True,
        help_text="Timestamp when the quiz was created"
    )

    # Yeh batata hai ki quiz baccho ke liye active (chalu) hai ya nahi
    is_active = models.BooleanField(
        # default=True ka matlab har nayi quiz by default active rahegi
        default=True, 
        help_text="Whether this quiz is published and accessible to students"
    )

    # Meta class database table ki additional settings define karti hai
    class Meta:
        # Django Admin mein single object ka naam kya dikhega
        verbose_name = "Quiz"
        # Django Admin mein plural (multiple objects) ka naam kya dikhega
        verbose_name_plural = "Quizzes"
        # Nayi quiz sabse upar dikhe isliye created_at ke aage '-' lagaya hai (descending order)
        ordering = ['-created_at']

    # Jab bhi Django is Quiz object ko print karega ya Admin panel mein dikhayega, toh title return hoga
    def __str__(self):
        # Admin panel mein object ka naam Quiz Object (1) ki jagah Quiz ka Title dikhega
        return self.title

    # Helper property jisse hum kisi bhi quiz ke total questions aasani se count kar sakein
    @property
    def total_questions(self):
        # self.questions.count() is quiz se jude saare questions ki ginti (count) return karega
        return self.questions.count()


# ==============================================================================
# 2. QUESTION MODEL (Table: quiz_question)
# ==============================================================================
# Yeh class har ek Multiple Choice Question (MCQ) ko store karne ke liye hai
class Question(models.Model):
    # Correct answer choose karne ke liye dropdown options ki list
    ANSWER_CHOICES = [
        ('option1', 'Option 1'),
        ('option2', 'Option 2'),
        ('option3', 'Option 3'),
        ('option4', 'Option 4'),
    ]

    # Yeh sawal kis Quiz ka hissa hai, uske liye ForeignKey (One-to-Many Relationship)
    quiz = models.ForeignKey(
        # Quiz model ke sath relation banaya gaya hai
        Quiz, 
        # on_delete=models.CASCADE ka matlab agar Quiz delete ho, toh uske saare sawal bhi apne aap delete ho jayein
        on_delete=models.CASCADE, 
        # related_name='questions' se hum quiz.questions.all() likhkar saare sawal nikal sakte hain
        related_name='questions',
        help_text="The quiz this question belongs to"
    )

    # Sawal ka actual text (Problem statement / Question prompt)
    question_text = models.TextField(
        help_text="The question prompt or problem statement"
    )

    # Pehla vikalp (Option 1 text)
    option1 = models.CharField(
        max_length=255, 
        help_text="First multiple choice option"
    )

    # Doosra vikalp (Option 2 text)
    option2 = models.CharField(
        max_length=255, 
        help_text="Second multiple choice option"
    )

    # Teesri vikalp (Option 3 text)
    option3 = models.CharField(
        max_length=255, 
        help_text="Third multiple choice option"
    )

    # Chautha vikalp (Option 4 text)
    option4 = models.CharField(
        max_length=255, 
        help_text="Fourth multiple choice option"
    )

    # In 4 options mein se kaunsa sahi hai ('option1', 'option2', 'option3', 'option4')
    correct_answer = models.CharField(
        max_length=10, 
        # choices=ANSWER_CHOICES se admin panel mein dropdown ban jata hai
        choices=ANSWER_CHOICES, 
        help_text="Select which option is the correct answer"
    )

    # Meta settings for Question
    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"

    # Admin panel mein question pehchanne ke liye Quiz ka naam aur question text ke pehle 50 characters dikhayenge
    def __str__(self):
        return f"{self.quiz.title} - {self.question_text[:50]}"

    # Yeh helper method sahi option ka text (jaise ".py" ya "def") return karta hai
    def get_correct_answer_text(self):
        # getattr dynamically us option field ki value uthata hai jo correct_answer mein set hai
        return getattr(self, self.correct_answer, '')
