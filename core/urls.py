from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views

urlpatterns = [
    # Auth
    path('register/', views.RegisterView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Courses & Lessons
    path('courses/', views.CourseListView.as_view(), name='course-list'),
    path('lessons/', views.LessonListView.as_view(), name='lesson-list'),
    path('lessons/<int:pk>/complete/', views.LessonCompleteView.as_view(), name='lesson-complete'),

    # Quiz
    path('lessons/<int:pk>/quiz/', views.LessonQuizView.as_view(), name='lesson-quiz'),
    path('quizzes/<int:pk>/submit/', views.QuizSubmitView.as_view(), name='quiz-submit'),

    # AI Tutor
    path('ai-tutor/', views.AITutorView.as_view(), name='ai-tutor'),
]
