from django.test import TestCase, Client
from django.urls import reverse
from .models import Quiz, Question


class QuizModelTests(TestCase):
    """Unit tests for Quiz and Question models."""

    def setUp(self):
        self.quiz = Quiz.objects.create(
            title="Test Quiz",
            description="Testing quiz description",
            is_active=True
        )
        self.question1 = Question.objects.create(
            quiz=self.quiz,
            question_text="What is 2 + 2?",
            option1="3",
            option2="4",
            option3="5",
            option4="6",
            correct_answer="option2"
        )

    def test_quiz_str(self):
        self.assertEqual(str(self.quiz), "Test Quiz")

    def test_question_str(self):
        self.assertIn("Test Quiz", str(self.question1))

    def test_quiz_total_questions(self):
        self.assertEqual(self.quiz.total_questions, 1)

    def test_question_correct_answer_text(self):
        self.assertEqual(self.question1.get_correct_answer_text(), "4")


class QuizViewTests(TestCase):
    """Unit tests for Quiz views and score calculation."""

    def setUp(self):
        self.client = Client()
        self.quiz = Quiz.objects.create(
            title="Python Testing Quiz",
            description="A quiz to test our views and submission logic",
            is_active=True
        )
        self.q1 = Question.objects.create(
            quiz=self.quiz,
            question_text="Question 1 text",
            option1="A",
            option2="B",
            option3="C",
            option4="D",
            correct_answer="option1"
        )
        self.q2 = Question.objects.create(
            quiz=self.quiz,
            question_text="Question 2 text",
            option1="W",
            option2="X",
            option3="Y",
            option4="Z",
            correct_answer="option3"
        )

    def test_home_page_status(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_quiz_list_page_status(self):
        response = self.client.get(reverse('quiz_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Python Testing Quiz")
        self.assertTemplateUsed(response, 'quiz_list.html')

    def test_quiz_detail_page_status(self):
        response = self.client.get(reverse('quiz_detail', args=[self.quiz.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Question 1 text")
        self.assertContains(response, "Question 2 text")
        self.assertTemplateUsed(response, 'quiz_detail.html')

    def test_quiz_detail_404_for_inactive_quiz(self):
        inactive_quiz = Quiz.objects.create(title="Inactive", description="Desc", is_active=False)
        response = self.client.get(reverse('quiz_detail', args=[inactive_quiz.id]))
        self.assertEqual(response.status_code, 404)

    def test_submit_quiz_full_score(self):
        post_data = {
            f'question_{self.q1.id}': 'option1',
            f'question_{self.q2.id}': 'option3',
        }
        response = self.client.post(reverse('submit_quiz', args=[self.quiz.id]), data=post_data)
        # Should redirect to result page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('result'))

        # Check session data
        session = self.client.session
        result_data = session.get('quiz_result')
        self.assertIsNotNone(result_data)
        self.assertEqual(result_data['total_questions'], 2)
        self.assertEqual(result_data['correct_answers'], 2)
        self.assertEqual(result_data['wrong_answers'], 0)
        self.assertEqual(result_data['percentage'], 100.0)

    def test_submit_quiz_partial_score(self):
        post_data = {
            f'question_{self.q1.id}': 'option1',  # Correct
            f'question_{self.q2.id}': 'option2',  # Wrong
        }
        response = self.client.post(reverse('submit_quiz', args=[self.quiz.id]), data=post_data)
        self.assertEqual(response.status_code, 302)

        session = self.client.session
        result_data = session.get('quiz_result')
        self.assertEqual(result_data['correct_answers'], 1)
        self.assertEqual(result_data['wrong_answers'], 1)
        self.assertEqual(result_data['percentage'], 50.0)

    def test_result_page_with_session(self):
        session = self.client.session
        session['quiz_result'] = {
            'quiz_id': self.quiz.id,
            'quiz_title': self.quiz.title,
            'total_questions': 2,
            'correct_answers': 2,
            'wrong_answers': 0,
            'unanswered': 0,
            'score': 2,
            'percentage': 100.0,
            'breakdown': []
        }
        session.save()

        response = self.client.get(reverse('result'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "100")
        self.assertContains(response, "Quiz Completed")
        self.assertTemplateUsed(response, 'result.html')
