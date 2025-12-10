# courses/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile, Course, Enrollment, Instructor, Student, Lesson, LessonProgress

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'role', 'is_active', 'date_joined']
    list_filter = ['role', 'is_active', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {
            'fields': ('role', 'phone_number')
        }),
    )

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number', 'created_at']

@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ['user', 'specialization', 'is_approved']
    list_filter = ['is_approved', 'specialization']

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_username', 'get_enrolled_courses_count']
    search_fields = ['user__username', 'user__email']
    filter_horizontal = ['enrolled_courses']  # إضافة هذه السطر
    
    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'
    
    def get_enrolled_courses_count(self, obj):
        return obj.enrolled_courses.count()
    get_enrolled_courses_count.short_description = 'Enrolled Courses'
    
    # إضافة هذه الدالة لتحديد كيفية عرض حقل user في نموذج الإضافة
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            # عرض فقط المستخدمين الذين لديهم دور student ولم يتم ربطهم بطلاب بعد
            kwargs["queryset"] = CustomUser.objects.filter(role='student')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'instructor', 'category', 'price', 'is_active', 'created_at']
    list_filter = ['is_active', 'is_paid', 'is_featured', 'category']
    search_fields = ['title', 'description']
    list_editable = ['is_active', 'price']

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order', 'duration']
    list_filter = ['course']
    ordering = ['course', 'order']

@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ['student', 'lesson', 'completed', 'completed_at']
    list_filter = ['completed', 'completed_at']

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'enrolled_at']
    list_filter = ['enrolled_at']