from django.contrib import admin
from .models import Course, Lesson, Quiz, Progress


class LessonInline(admin.TabularInline):
    """Inline editor for lessons within a course."""
    model = Lesson
    extra = 1
    fields = ('title', 'order', 'thumbnail_url', 'content')
    ordering = ('order',)


class QuizInline(admin.TabularInline):
    """Inline editor for quizzes within a lesson."""
    model = Quiz
    extra = 1
    fields = ('question', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_option')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'lesson_count', 'created_at')
    search_fields = ('title', 'description')
    inlines = [LessonInline]

    def lesson_count(self, obj):
        return obj.lessons.count()
    lesson_count.short_description = 'Lessons'


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    list_filter = ('course',)
    search_fields = ('title', 'content')
    ordering = ('course', 'order')
    inlines = [QuizInline]


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('question_preview', 'lesson', 'correct_option')
    list_filter = ('lesson__course', 'correct_option')
    search_fields = ('question',)

    def question_preview(self, obj):
        return obj.question[:80] + ('...' if len(obj.question) > 80 else '')
    question_preview.short_description = 'Question'


@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'completed', 'updated_at')
    list_filter = ('completed', 'lesson__course')
    search_fields = ('user__username', 'lesson__title')
