# courses/models.py
from django.contrib.auth.models import AbstractUser  # تأكدي من هذا السطر
from django.db import models

class CustomUser(AbstractUser):  # كان فيه خطأ في الكتابة
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('instructor', 'Instructor'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='customuser_set',  # غيري related_name
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='customuser_set',  # غيري related_name
        related_query_name='user',
    )
    
    def __str__(self):
        return self.username
    
    @property
    def is_student(self):
        return self.role == 'student'
    
    @property
    def is_instructor(self):
        return self.role == 'instructor'
    
    @property
    def is_admin(self):
        return self.role == 'admin' or self.is_superuser

# باقي الموديلات غيري User لـ CustomUser
class Instructor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    bio = models.TextField()
    specialization = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='instructors/', blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    is_approved = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Instructor: {self.user.username}"
    
    @property
    def total_courses(self):
        return self.course_set.count()
    
    @property
    def total_students(self):
        from django.db.models import Count
        return self.course_set.aggregate(total=Count('enrolled_students'))['total'] or 0

class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,limit_choices_to={'role': 'student'} )
    enrolled_courses = models.ManyToManyField('Course', blank=True, related_name='enrolled_students')
    
    def __str__(self):
        return f"Student: {self.user.username}"
    
    def get_completed_lessons_count(self, course):
        return LessonProgress.objects.filter(
            student=self, 
            lesson__course=course, 
            completed=True
        ).count()
    
    def get_course_progress(self, course):
        total_lessons = course.total_lessons
        if total_lessons == 0:
            return 0
        completed_lessons = self.get_completed_lessons_count(course)
        return (completed_lessons / total_lessons) * 100

# باقي الموديلات تفضل كما هي مع تغيير User لـ CustomUser
class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    thumbnail = models.ImageField(upload_to='course_thumbnails/', blank=True, null=True)
    category = models.CharField(max_length=100, default='Development')
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
    
    @property
    def total_lessons(self):
        return self.lesson_set.count()
    
    @property
    def total_enrollments(self):
        return self.enrolled_students.count()

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    video_url = models.URLField(blank=True)
    order = models.IntegerField(default=0)
    duration = models.IntegerField(default=0, help_text="Duration in minutes")
    
    class Meta:
        ordering = ['order']
        
    def __str__(self):
        return f"{self.order}. {self.title} - {self.course.title}"

class LessonProgress(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='lesson_progress')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='student_progress')
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ['student', 'lesson']
        
    def __str__(self):
        return f"{self.student.user.username} - {self.lesson.title}"

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['student', 'course']
    
    def __str__(self):
        return f"{self.student.user.username} - {self.course.title}"

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='user_profile')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Profile of {self.user.username}"
    
    @property
    def is_admin(self):
        return self.user.is_superuser
    
    @property
    def is_instructor(self):
        return hasattr(self.user, 'instructor')
    
    @property
    def is_student(self):
        return hasattr(self.user, 'student')

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'user_profile'):
        instance.user_profile.save()