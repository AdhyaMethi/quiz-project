# Django ke helper functions:
# render: HTML template ko context data ke sath render karke web page banane ke liye
# get_object_or_404: Database se record nikalta hai, agar nahi mile toh 404 page dikhata hai
# redirect: User ko kisi doosre URL/page par bhejne ke liye
from django.shortcuts import render, get_object_or_404, redirect

# User ko success, warning ya error alerts dikhane ke liye Django messages framework
from django.contrib import messages

# Hamare models.py se Quiz aur Question classes ko import kar rahe hain
from .models import Quiz, Question


# ==============================================================================
# 1. HOME VIEW (Landing Page)
# ==============================================================================
# Jab user website ke main URL '/' par aata hai tab yeh function chalta hai
def home(request):
    # Database se count nikaal rahe hain ki kitni Active Quizzes maujood hain
    total_quizzes = Quiz.objects.filter(is_active=True).count()

    # Active Quizzes se jude total questions ki sankhya count kar rahe hain
    total_questions = Question.objects.filter(quiz__is_active=True).count()

    # Data ka dictionary bana rahe hain jo home.html template ko bheja jayega
    context = {
        'total_quizzes': total_quizzes,       # Total active quizzes template variable
        'total_questions': total_questions,   # Total questions template variable
    }

    # 'home.html' template ko context data ke sath browser ko bhej rahe hain
    return render(request, 'home.html', context)


# ==============================================================================
# 2. QUIZ LIST VIEW (All Active Quizzes)
# ==============================================================================
# Jab user '/quizzes/' page kholta hai tab yeh function chalta hai
def quiz_list(request):
    # Database se sirf wahi quizzes fetch kar rahe hain jinka is_active = True hai
    # prefetch_related('questions') performance optimize karta hai taki SQL queries kam chalein
    quizzes = Quiz.objects.filter(is_active=True).prefetch_related('questions')

    # Template ko bhejne ke liye data dictionary
    context = {
        'quizzes': quizzes, # Active quizzes ki QuerySet list
    }

    # 'quiz_list.html' template ko render karke user ko dikha rahe hain
    return render(request, 'quiz_list.html', context)


# ==============================================================================
# 3. QUIZ DETAIL VIEW (Questions & MCQ Form)
# ==============================================================================
# Jab student kisi quiz ke 'Start Quiz' button par click karta hai (/quiz/1/)
def quiz_detail(request, quiz_id):
    # Diye gaye quiz_id se quiz dhoondh rahe hain; agar quiz inactive ya galat ID ho toh 404 error aayega
    quiz = get_object_or_404(Quiz, id=quiz_id, is_active=True)

    # Is quiz ke andar aane wale saare questions ko database se nikaal rahe hain
    questions = quiz.questions.all()

    # Check kar rahe hain ki kya is quiz mein kam se kam 1 question hai ya nahi
    has_questions = questions.exists()

    # Template ke liye context dictionary tayyar kar rahe hain
    context = {
        'quiz': quiz,                   # Quiz object details (Title, Description)
        'questions': questions,         # Is quiz ke saare questions ki list
        'has_questions': has_questions, # Boolean flag (True/False)
    }

    # 'quiz_detail.html' template render karke student ko questions dikhayenge
    return render(request, 'quiz_detail.html', context)


# ==============================================================================
# 4. SUBMIT QUIZ VIEW (Score Calculation & Session Storage)
# ==============================================================================
# Jab student submit button dabata hai toh POST request yahan aati hai (/quiz/1/submit/)
def submit_quiz(request, quiz_id):
    # Security check: Agar koi user direct URL kholne ki koshish kare (GET request), toh wapas bhej do
    if request.method != 'POST':
        # User ko wapas usi quiz ke question page par redirect kar dete hain
        return redirect('quiz_detail', quiz_id=quiz_id)

    # Database se quiz object retrieve kar rahe hain
    quiz = get_object_or_404(Quiz, id=quiz_id, is_active=True)

    # Quiz ke saare questions database se fetch kar rahe hain
    questions = quiz.questions.all()

    # Total kitne questions the, unki ginti kar rahe hain
    total_questions = questions.count()

    # Edge Case: Agar quiz mein ek bhi question nahi hai
    if total_questions == 0:
        # Warning flash message set kar rahe hain
        messages.warning(request, "This quiz does not contain any questions yet.")
        # User ko quiz catalogue list par wapas bhej dete hain
        return redirect('quiz_list')

    # Sahi jawabo (Correct Answers) ka counter initialize kar rahe hain
    correct_answers = 0

    # Galat jawabo (Wrong Answers) ka counter initialize kar rahe hain
    wrong_answers = 0

    # Chhute huye jawabo (Unanswered) ka counter initialize kar rahe hain
    unanswered = 0

    # Result page par question-by-question review dikhane ke liye list
    question_breakdown = []

    # Har ek question par loop chala kar student ka answer check karte hain
    for question in questions:
        # Form field ka naam HTML mein 'question_{id}' rakha gaya tha (jaise question_1, question_2)
        field_name = f'question_{question.id}'

        # POST data se student dwara chuna hua option value nikaal rahe hain (jaise 'option1')
        selected_option = request.POST.get(field_name)

        # Chune gaye option ka actual text nikaal rahe hain (jaise ".py" ya "No Answer Selected")
        selected_text = getattr(question, selected_option, 'No Answer Selected') if selected_option else 'No Answer Selected'

        # Sahi option ka actual text nikaal rahe hain
        correct_text = getattr(question, question.correct_answer, '')

        # Check: Kya student ka chuna option database ke correct_answer ke barabar hai?
        if selected_option and selected_option == question.correct_answer:
            # Agar barabar hai toh answer sahi hai
            is_correct = True
            # Correct counter ko 1 se badha do
            correct_answers += 1
        else:
            # Agar match nahi hua ya answer nahi diya toh answer galat hai
            is_correct = False
            # Wrong counter ko 1 se badha do
            wrong_answers += 1
            # Agar student ne option select hi nahi kiya tha
            if not selected_option:
                # Unanswered counter ko 1 se badha do
                unanswered += 1

        # Is question ki review detail breakdown list mein append kar rahe hain
        question_breakdown.append({
            'question_text': question.question_text,    # Sawal kya tha
            'selected_option': selected_option,          # Student ne kya select kiya
            'selected_text': selected_text,              # Student ke option ka text
            'correct_option': question.correct_answer,   # Asli sahi option kaunsa tha
            'correct_text': correct_text,                # Asli sahi option ka text
            'is_correct': is_correct,                    # Sahi tha ya galat (True/False)
        })

    # Formula se Percentage calculate kar rahe hain: (Correct / Total) * 100
    percentage = round((correct_answers / total_questions) * 100, 1)

    # Score aur result details ko Django Session mein securely save kar rahe hain
    request.session['quiz_result'] = {
        'quiz_id': quiz.id,                         # Quiz ID
        'quiz_title': quiz.title,                   # Quiz Title
        'total_questions': total_questions,         # Total Questions
        'correct_answers': correct_answers,         # Total Correct
        'wrong_answers': wrong_answers,             # Total Wrong
        'unanswered': unanswered,                   # Total Unanswered
        'score': correct_answers,                   # Final Score
        'percentage': percentage,                   # Score Percentage %
        'breakdown': question_breakdown,            # Full answer review
    }

    # Score calculate hone ke baad user ko dedicated '/result/' page par redirect kar rahe hain
    return redirect('result')


# ==============================================================================
# 5. RESULT VIEW (Display Final Scorecard)
# ==============================================================================
# Submit hone ke baad user ko final scorecard dikhane wala function
def result(request):
    # Session se pichli quiz ka result data nikaal rahe hain
    result_data = request.session.get('quiz_result')

    # Agar session mein koi result data nahi mila (user ne bina quiz attempt kiye URL khola)
    if not result_data:
        # Information alert bhej rahe hain
        messages.info(request, "No recent quiz results found. Please select and complete a quiz first.")
        # User ko quiz catalogue list par redirect kar dete hain
        return redirect('quiz_list')

    # Percentage ke hisab se performance grade aur message tayyar kar rahe hain
    percentage = result_data.get('percentage', 0)

    # Agar score 90% ya usse zyada hai
    if percentage >= 90:
        feedback_message = "Outstanding! You have mastered this topic!"
        feedback_grade = "Excellent"
        feedback_class = "grade-excellent"
    # Agar score 70% se 89% ke beech hai
    elif percentage >= 70:
        feedback_message = "Great job! You demonstrated solid knowledge."
        feedback_grade = "Good"
        feedback_class = "grade-good"
    # Agar score 50% se 69% ke beech hai
    elif percentage >= 50:
        feedback_message = "Fair effort! Review the questions and try again to improve."
        feedback_grade = "Average"
        feedback_class = "grade-average"
    # Agar score 50% se kam hai
    else:
        feedback_message = "Don't give up! Study the concepts and give it another shot."
        feedback_grade = "Needs Practice"
        feedback_class = "grade-practice"

    # Context dictionary bana rahe hain jo result.html ko pass hogi
    context = {
        'result': result_data,                      # Session se aaya result dictionary
        'feedback_message': feedback_message,        # Motivational message
        'feedback_grade': feedback_grade,            # Grade (Excellent/Good/etc)
        'feedback_class': feedback_class,            # CSS styling class for colors
    }

    # 'result.html' template render karke scorecard dikha rahe hain
    return render(request, 'result.html', context)
