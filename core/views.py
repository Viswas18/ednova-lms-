import logging
# pyrefly: ignore [missing-import]
from django.conf import settings
# pyrefly: ignore [missing-import]
from rest_framework import generics, status
# pyrefly: ignore [missing-import]
from rest_framework.views import APIView
# pyrefly: ignore [missing-import]
from rest_framework.response import Response
# pyrefly: ignore [missing-import]
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Course, Lesson, Quiz, Progress
from .serializers import (
    RegisterSerializer,
    CourseSerializer,
    LessonSerializer,
    QuizSerializer,
    QuizSubmitSerializer,
    AITutorSerializer,
)

logger = logging.getLogger(__name__)


# ─── Authentication ───────────────────────────────────────────────

class RegisterView(generics.CreateAPIView):
    """POST /api/register/ — Create a new user account."""
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


# ─── Course & Lesson Delivery ────────────────────────────────────

class CourseListView(generics.ListAPIView):
    """GET /api/courses/ — List all available courses."""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]


class LessonListView(generics.ListAPIView):
    """GET /api/lessons/?course_id=<id> — Lessons for a specific course."""
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        course_id = self.request.query_params.get('course_id')
        if course_id:
            return Lesson.objects.filter(course_id=course_id)
        return Lesson.objects.all()


class LessonCompleteView(APIView):
    """POST /api/lessons/<id>/complete/ — Mark a lesson as completed."""
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            lesson = Lesson.objects.get(pk=pk)
        except Lesson.DoesNotExist:
            return Response(
                {"error": "Lesson not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        progress, created = Progress.objects.get_or_create(
            user=request.user,
            lesson=lesson,
            defaults={'completed': True}
        )
        if not created:
            progress.completed = True
            progress.save()

        return Response({
            "message": "Lesson marked as completed.",
            "completed": True
        })


# ─── Interactive Quiz System ─────────────────────────────────────

class LessonQuizView(APIView):
    """GET /api/lessons/<id>/quiz/ — Fetch quiz questions for a lesson."""
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        quizzes = Quiz.objects.filter(lesson_id=pk)
        if not quizzes.exists():
            return Response(
                {"error": "No quiz found for this lesson."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = QuizSerializer(quizzes, many=True)
        return Response(serializer.data)


class QuizSubmitView(APIView):
    """POST /api/quizzes/<id>/submit/ — Submit an answer and check correctness."""
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            quiz = Quiz.objects.get(pk=pk)
        except Quiz.DoesNotExist:
            return Response(
                {"error": "Quiz not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = QuizSubmitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        selected = serializer.validated_data['selected_option']
        is_correct = selected == quiz.correct_option

        return Response({
            "correct": is_correct,
            "selected_option": selected,
            "correct_option": quiz.correct_option if is_correct else None,
            "message": "Correct! 🎉" if is_correct else "Incorrect. Try again!"
        })


# ─── AI Tutor ────────────────────────────────────────────────────

class AITutorView(APIView):
    """
    POST /api/ai-tutor/
    Payload: {"lesson_id": 1, "message": "Explain this simply."}
    
    Uses Google Gemini API to provide contextual tutoring grounded
    in the lesson content.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AITutorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        lesson_id = serializer.validated_data['lesson_id']
        user_message = serializer.validated_data['message']

        # Fetch lesson context
        try:
            lesson = Lesson.objects.get(pk=lesson_id)
        except Lesson.DoesNotExist:
            return Response(
                {"error": "Lesson not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        api_key = settings.AI_API_KEY
        if not api_key or api_key == 'your-api-key-here':
            return Response({
                "reply": "🤖 The AI Tutor is currently taking a break! Please try again later or reach out to your instructor if you need help."
            })

        # Build the system prompt with lesson context
        system_prompt = (
            f"You are an expert, friendly AI tutor for an online learning platform called EdNova. "
            f"You are helping a student with the following lesson:\n\n"
            f"**Lesson Title:** {lesson.title}\n\n"
            f"**Lesson Content:**\n{lesson.content}\n\n"
            f"Instructions:\n"
            f"- Answer the student's question based on the lesson content above.\n"
            f"- Be concise, clear, and encouraging.\n"
            f"- Use simple analogies when explaining complex concepts.\n"
            f"- If the question is unrelated to the lesson, gently redirect them.\n"
            f"- Format your response with markdown for readability."
        )

        try:
            from google import genai

            client = genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[
                    {"role": "user", "parts": [{"text": system_prompt + "\n\nStudent's question: " + user_message}]}
                ]
            )

            reply = response.text
            return Response({"reply": reply})

        except Exception as e:
            logger.error(f"AI Tutor error: {e}")
            return Response(
                {"reply": f"⚠️ AI Tutor encountered an error. Please try again later. ({type(e).__name__})"},
                status=status.HTTP_200_OK
            )
