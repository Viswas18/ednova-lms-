from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Course, Lesson, Quiz, Progress


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    """Read-only user info."""
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class CourseSerializer(serializers.ModelSerializer):
    """Course listing with lesson count."""
    lesson_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ('id', 'title', 'description', 'thumbnail_url', 'icon_emoji', 'lesson_count', 'created_at')

    def get_lesson_count(self, obj):
        return obj.lessons.count()


class LessonSerializer(serializers.ModelSerializer):
    """Lesson with completion status for the requesting user."""
    is_completed = serializers.SerializerMethodField()
    has_quiz = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ('id', 'course', 'title', 'content', 'thumbnail_url', 'order', 'is_completed', 'has_quiz')

    def get_is_completed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Progress.objects.filter(
                user=request.user,
                lesson=obj,
                completed=True
            ).exists()
        return False

    def get_has_quiz(self, obj):
        return obj.quizzes.exists()


class QuizSerializer(serializers.ModelSerializer):
    """Quiz serializer — correct_option is EXCLUDED to prevent cheating."""
    class Meta:
        model = Quiz
        fields = ('id', 'lesson', 'question', 'option_a', 'option_b', 'option_c', 'option_d')
        # NOTE: correct_option intentionally excluded


class QuizSubmitSerializer(serializers.Serializer):
    """Validates quiz answer submission."""
    selected_option = serializers.ChoiceField(choices=['A', 'B', 'C', 'D'])


class ProgressSerializer(serializers.ModelSerializer):
    """Read-only progress tracking."""
    lesson_title = serializers.CharField(source='lesson.title', read_only=True)

    class Meta:
        model = Progress
        fields = ('id', 'lesson', 'lesson_title', 'completed', 'updated_at')


class AITutorSerializer(serializers.Serializer):
    """Validates AI tutor request."""
    lesson_id = serializers.IntegerField()
    message = serializers.CharField(max_length=2000)
