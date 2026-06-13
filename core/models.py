from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):
    """Primary grouping object for lessons."""
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    thumbnail_url = models.URLField(
        blank=True, default='',
        help_text="URL to a course thumbnail image (e.g. from Unsplash)."
    )
    icon_emoji = models.CharField(
        max_length=10, default='📚',
        help_text="Emoji icon for the course."
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def lesson_count(self):
        return self.lessons.count()


class Lesson(models.Model):
    """Contains text-based learning material within a course."""
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons'
    )
    title = models.CharField(max_length=255)
    content = models.TextField(
        help_text="Lesson content. Supports Markdown formatting."
    )
    thumbnail_url = models.URLField(
        blank=True, default='',
        help_text="URL to a lesson thumbnail image."
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} → {self.title}"


class Quiz(models.Model):
    """4-choice MCQ linked to a lesson."""
    OPTION_CHOICES = [
        ('A', 'Option A'),
        ('B', 'Option B'),
        ('C', 'Option C'),
        ('D', 'Option D'),
    ]

    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='quizzes'
    )
    question = models.TextField()
    option_a = models.CharField(max_length=500)
    option_b = models.CharField(max_length=500)
    option_c = models.CharField(max_length=500)
    option_d = models.CharField(max_length=500)
    correct_option = models.CharField(
        max_length=1,
        choices=OPTION_CHOICES,
        help_text="The correct answer (A, B, C, or D)."
    )

    class Meta:
        verbose_name_plural = "Quizzes"

    def __str__(self):
        return f"Quiz: {self.question[:60]}..."


class Progress(models.Model):
    """Tracks if a user completed a specific lesson."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='progress'
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='progress'
    )
    completed = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'lesson')
        verbose_name_plural = "Progress records"

    def __str__(self):
        status = "✅" if self.completed else "⬜"
        return f"{status} {self.user.username} — {self.lesson.title}"
