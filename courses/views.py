# courses/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Avg, Count
from .models import Course, Lesson, Student, Instructor, LessonProgress, Enrollment, UserProfile
from .decorators import admin_required, instructor_required

# ========== النظام الحالي - بدون تغيير ==========

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    lessons = Lesson.objects.filter(course=course).order_by('order')
    
    is_enrolled = False
    completed_lessons = []
    progress_percentage = 0
    completed_count = 0
    total_lessons = lessons.count()
    
    if request.user.is_authenticated and hasattr(request.user, 'student'):
        is_enrolled = request.user.student.enrolled_courses.filter(id=course_id).exists()
        
        if is_enrolled:
            completed_lessons = LessonProgress.objects.filter(
                student=request.user.student,
                lesson__course=course,
                completed=True
            ).values_list('lesson_id', flat=True)
            
            completed_count = len(completed_lessons)
            if total_lessons > 0:
                progress_percentage = int((completed_count / total_lessons) * 100)
    
    return render(request, 'courses/course_detail.html', {
        'course': course,
        'lessons': lessons,
        'is_enrolled': is_enrolled,
        'completed_lessons': list(completed_lessons),
        'progress_percentage': progress_percentage,
        'completed_count': completed_count,
        'total_lessons': total_lessons,
    })

def create_sample_courses():
    """إنشاء كورسات تجريبية إذا لم تكن موجودة"""
    try:
        instructor_user = User.objects.filter(is_superuser=True).first()
        if not instructor_user:
            instructor_user = User.objects.create_user(
                username='admin_instructor',
                email='admin@elearn.com',
                password='admin123'
            )
        
        instructor, created = Instructor.objects.get_or_create(user=instructor_user)
        
        sample_courses = [
            {
                'title': 'Web Development with Django & React',
                'description': 'Complete course to learn full-stack web development from beginner to advanced level. Build real-world projects and master modern web technologies.',
                'price': 0.00,
                'is_paid': False,
                'image_url': 'https://cdn.pixabay.com/photo/2020/05/18/16/17/social-media-5187243_1280.png'
            },
            {
                'title': 'Python Programming Mastery',
                'description': 'Learn Python from basics to advanced topics including OOP, data structures, APIs, and web development with Django.',
                'price': 99.00,
                'is_paid': True,
                'image_url': 'https://cdn.pixabay.com/photo/2016/03/27/18/54/technology-1283624_1280.jpg'
            },
            {
                'title': 'Data Science Fundamentals',
                'description': 'Master data analysis, machine learning, statistics, and Python for data science. Work with real datasets and build predictive models.',
                'price': 149.00,
                'is_paid': True,
                'image_url': 'https://cdn.pixabay.com/photo/2018/05/08/08/44/artificial-intelligence-3382507_1280.jpg'
            }
        ]
        
        created_courses = []
        for i, course_data in enumerate(sample_courses, 1):
            course, created = Course.objects.get_or_create(
                title=course_data['title'],
                defaults={
                    'description': course_data['description'],
                    'instructor': instructor,
                    'price': course_data['price'],
                    'is_paid': course_data['is_paid']
                }
            )
            
            if created:
                lessons_data = [
                    {'title': 'Introduction to the Course', 'content': 'Welcome and course overview', 'order': 1},
                    {'title': 'Getting Started', 'content': 'Setup development environment', 'order': 2},
                    {'title': 'Core Concepts', 'content': 'Learn fundamental concepts and techniques', 'order': 3},
                    {'title': 'Hands-on Projects', 'content': 'Build real-world applications', 'order': 4},
                    {'title': 'Advanced Topics', 'content': 'Dive deeper into advanced concepts', 'order': 5},
                ]
                
                for lesson_data in lessons_data:
                    Lesson.objects.create(
                        course=course,
                        title=lesson_data['title'],
                        content=lesson_data['content'],
                        order=lesson_data['order']
                    )
                
                created_courses.append(course)
        
        return created_courses
    except Exception as e:
        print(f"Error creating sample courses: {e}")
        return []

def home(request):
    if Course.objects.count() == 0:
        create_sample_courses()
    
    total_courses = Course.objects.count()
    total_students = Student.objects.count()
    total_instructors = Instructor.objects.count()
    
    featured_courses = [
        {
            'id': 1,
            'title': 'Web Development with Django & React',
            'description': 'Complete course to learn full-stack web development from beginner to advanced level',
            'image': 'https://cdn.pixabay.com/photo/2020/05/18/16/17/social-media-5187243_1280.png',
            'instructor': {'user': {'username': 'prof_ahmed'}},
            'is_paid': False,
            'price': 0,
            'rating': 4.7,
            'reviews': 1234,
            'students': 5432
        },
        {
            'id': 2,
            'title': 'Complete Web Development Bootcamp 2025',
            'description': 'Learn HTML, CSS, JavaScript, React, Node.js, and MongoDB. Build 10+ real projects',
            'image': 'https://cdn.pixabay.com/photo/2016/11/19/22/25/code-1841550_1280.jpg',
            'instructor': {'user': {'username': 'emma_wilson'}},
            'is_paid': True,
            'price': 299.00,
            'rating': 4.9,
            'reviews': 2567,
            'students': 8921
        },
        {
            'id': 3,
            'title': 'Cybersecurity Fundamentals',
            'description': 'Network security, ethical hacking, penetration testing, and security protocols',
            'image': 'https://cdn.pixabay.com/photo/2018/05/08/08/44/artificial-intelligence-3382507_1280.jpg',
            'instructor': {'user': {'username': 'dr_sarah'}},
            'is_paid': True,
            'price': 279.00,
            'rating': 4.8,
            'reviews': 1876,
            'students': 4215
        }
    ]
    
    return render(request, 'courses/home.html', {
        'featured_courses': featured_courses,
        'total_courses': total_courses or 120,
        'total_students': total_students or 15000,
        'total_instructors': total_instructors or 85,
    })

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        account_type = request.POST['account_type']
        
        if password1 != password2:
            messages.error(request, "Passwords don't match")
            return redirect('signup')
        
        try:
            user = User.objects.create_user(username=username, email=email, password=password1)
            
            if account_type == 'student':
                Student.objects.create(user=user)
                messages.success(request, f"Student account created successfully! Welcome, {user.username}!")
            elif account_type == 'instructor':
                Instructor.objects.create(user=user)
                messages.success(request, f"Instructor account created successfully! Welcome, {user.username}!")
            
            login(request, user)
            return redirect('home')
            
        except Exception as e:
            messages.error(request, f"Error creating account: {str(e)}")
    
    return render(request, 'registration/signup.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {username}!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")
    
    return render(request, 'registration/login.html')

def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully")
    return redirect('home')

@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    if not hasattr(request.user, 'student'):
        messages.error(request, "Only students can enroll in courses")
        return redirect('course_detail', course_id=course_id)
    
    student = request.user.student
    student.enrolled_courses.add(course)
    messages.success(request, f"Successfully enrolled in {course.title}!")
    
    return redirect('course_detail', course_id=course_id)

@login_required
def my_courses(request):
    if hasattr(request.user, 'student'):
        courses = request.user.student.enrolled_courses.all()
        return render(request, 'courses/my_courses.html', {'courses': courses})
    else:
        messages.error(request, "Only students have enrolled courses")
        return redirect('course_list')

@login_required
def mark_lesson_complete(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    
    if not hasattr(request.user, 'student'):
        messages.error(request, "Only students can mark lessons as complete")
        return redirect('course_detail', course_id=lesson.course.id)
    
    if not request.user.student.enrolled_courses.filter(id=lesson.course.id).exists():
        messages.error(request, "You must be enrolled in the course to mark lessons as complete")
        return redirect('course_detail', course_id=lesson.course.id)
    
    progress, created = LessonProgress.objects.get_or_create(
        student=request.user.student,
        lesson=lesson,
        defaults={'completed': True}
    )
    if not created:
        progress.completed = True
        progress.save()
    
    messages.success(request, f"Lesson '{lesson.title}' marked as completed!")
    return redirect('course_detail', course_id=lesson.course.id)

# ========== النظام الجديد للادمن ==========

@login_required  
@admin_required
def admin_dashboard(request):
    from .models import CustomUser
    
    total_courses = Course.objects.count()
    total_students = CustomUser.objects.filter(role='student').count()
    total_instructors = CustomUser.objects.filter(role='instructor').count()
    total_enrollments = Enrollment.objects.count()
    
    courses = Course.objects.all().order_by('-created_at')[:10]
    
    context = {
        'total_courses': total_courses,
        'total_students': total_students, 
        'total_instructors': total_instructors,
        'total_enrollments': total_enrollments,
        'courses': courses,
    }
    return render(request, 'admin/dashboard.html', context)

@login_required
@admin_required
def admin_course_create(request):
    """إنشاء كورس جديد من قبل الادمن"""
    if request.method == 'POST':
        try:
            title = request.POST.get('title')
            description = request.POST.get('description')
            instructor_id = request.POST.get('instructor')
            price = request.POST.get('price', 0)
            is_paid = request.POST.get('is_paid') == 'on'
            category = request.POST.get('category', 'Development')
            is_active = request.POST.get('is_active') == 'on'
            is_featured = request.POST.get('is_featured') == 'on'
            thumbnail = request.FILES.get('thumbnail')
            
            instructor = Instructor.objects.get(id=instructor_id)
            
            course = Course.objects.create(
                title=title,
                description=description,
                instructor=instructor,
                price=price,
                is_paid=is_paid,
                category=category,
                is_active=is_active,
                is_featured=is_featured
            )
            
            if thumbnail:
                course.thumbnail = thumbnail
                course.save()
            
            messages.success(request, f"Course '{course.title}' created successfully!")
            return redirect('admin_dashboard')
            
        except Exception as e:
            messages.error(request, f"Error creating course: {str(e)}")
    
    instructors = Instructor.objects.all()
    return render(request, 'admin/courses/course_form.html', {'instructors': instructors})

@login_required
@admin_required
def admin_course_edit(request, course_id):
    """تعديل كورس من قبل الادمن"""
    course = get_object_or_404(Course, id=course_id)
    
    if request.method == 'POST':
        try:
            course.title = request.POST.get('title', course.title)
            course.description = request.POST.get('description', course.description)
            course.instructor = Instructor.objects.get(id=request.POST.get('instructor'))
            course.price = request.POST.get('price', course.price)
            course.is_paid = request.POST.get('is_paid') == 'on'
            course.category = request.POST.get('category', course.category)
            course.is_active = request.POST.get('is_active') == 'on'
            course.is_featured = request.POST.get('is_featured') == 'on'
            
            thumbnail = request.FILES.get('thumbnail')
            if thumbnail:
                course.thumbnail = thumbnail
            
            course.save()
            
            messages.success(request, f"Course '{course.title}' updated successfully!")
            return redirect('admin_dashboard')
            
        except Exception as e:
            messages.error(request, f"Error updating course: {str(e)}")
    
    instructors = Instructor.objects.all()
    return render(request, 'admin/courses/course_form.html', {
        'course': course,
        'instructors': instructors
    })

@login_required
@admin_required
def admin_course_delete(request, course_id):
    """حذف كورس من قبل الادمن"""
    course = get_object_or_404(Course, id=course_id)
    
    if request.method == 'POST':
        course_title = course.title
        course.delete()
        messages.success(request, f"Course '{course_title}' deleted successfully!")
        return redirect('admin_dashboard')
    
    return render(request, 'admin/courses/confirm_delete.html', {'course': course})

@login_required
@admin_required
def admin_instructors(request):
    """إدارة المدربين"""
    instructors = Instructor.objects.all().select_related('user')
    
    # حساب عدد الطلاب لكل مدرب
    for instructor in instructors:
        instructor.total_students_count = Student.objects.filter(
            enrolled_courses__instructor=instructor
        ).distinct().count()
    
    context = {
        'instructors': instructors,
    }
    return render(request, 'admin/instructors.html', context)

@login_required
@admin_required
def admin_students(request):
    """إدارة الطلاب"""
    students = Student.objects.all().select_related('user')
    
    # حساب عدد الكورسات لكل طالب
    for student in students:
        student.enrolled_courses_count = student.enrolled_courses.count()
    
    context = {
        'students': students,
    }
    return render(request, 'admin/students.html', context)

# ========== النظام الحالي للمدربين - بدون تغيير ==========

def instructor_profile(request, instructor_id):
    """صفحة البروفايل الخاصة بالمدرب"""
    instructor = get_object_or_404(Instructor, id=instructor_id)
    
    # إحصائيات المدرب
    instructor_stats = {
        'total_courses': instructor.course_set.count(),
        'total_students': Student.objects.filter(
            enrolled_courses__instructor=instructor
        ).distinct().count(),
        'total_lessons': Lesson.objects.filter(course__instructor=instructor).count(),
    }
    
    context = {
        'instructor': instructor,
        'stats': instructor_stats,
    }
    return render(request, 'instructors/instructor_profile.html', context)

@login_required
def instructor_dashboard(request):
    """لوحة تحكم المدرب"""
    try:
        instructor = Instructor.objects.get(user=request.user)
    except Instructor.DoesNotExist:
        messages.error(request, "You are not registered as an instructor")
        return redirect('home')
    
    # الكورسات الخاصة بهذا المدرب
    courses = Course.objects.filter(instructor=instructor)
    
    # إحصائيات المدرب
    total_students = Student.objects.filter(
        enrolled_courses__instructor=instructor
    ).distinct().count()
    
    total_lessons = Lesson.objects.filter(course__instructor=instructor).count()
    
    context = {
        'instructor': instructor,
        'courses': courses,
        'total_courses': courses.count(),
        'total_students': total_students,
        'total_lessons': total_lessons,
    }
    return render(request, 'instructors/instructor_dashboard.html', context)

@login_required
def create_course(request):
    """إنشاء كورس جديد"""
    try:
        instructor = Instructor.objects.get(user=request.user)
    except Instructor.DoesNotExist:
        messages.error(request, "You are not registered as an instructor")
        return redirect('home')
    
    if request.method == 'POST':
        try:
            # نجيب البيانات من الفورم
            title = request.POST.get('title')
            description = request.POST.get('description')
            price = request.POST.get('price', 0)
            is_paid = request.POST.get('is_paid') == 'on'
            category = request.POST.get('category', 'Development')
            thumbnail = request.FILES.get('thumbnail')
            
            # ننشئ الكورس
            course = Course.objects.create(
                title=title,
                description=description,
                instructor=instructor,
                price=price,
                is_paid=is_paid,
                category=category
            )
            
            # إذا في صورة نضيفها
            if thumbnail:
                course.thumbnail = thumbnail
                course.save()
            
            messages.success(request, f"Course '{course.title}' created successfully!")
            return redirect('instructor_dashboard')
            
        except Exception as e:
            messages.error(request, f"Error creating course: {str(e)}")
    
    # نعرض الفورم الفاضي
    return render(request, 'instructors/create_course.html')

@login_required
def edit_course(request, course_id):
    """تعديل كورس موجود"""
    try:
        instructor = Instructor.objects.get(user=request.user)
        course = get_object_or_404(Course, id=course_id, instructor=instructor)
    except Instructor.DoesNotExist:
        messages.error(request, "You are not registered as an instructor")
        return redirect('home')
    
    if request.method == 'POST':
        # هنا هتضيفي معالجة التعديل
        course.title = request.POST.get('title', course.title)
        course.description = request.POST.get('description', course.description)
        course.price = request.POST.get('price', course.price)
        course.is_paid = request.POST.get('is_paid') == 'on'
        course.category = request.POST.get('category', course.category)
        course.save()
        
        messages.success(request, f"Course '{course.title}' updated successfully!")
        return redirect('instructor_dashboard')
    
    context = {
        'course': course,
    }
    return render(request, 'instructors/edit_course.html', context)

@login_required
def become_instructor(request):
    """طلب الانضمام كمدرب"""
    if hasattr(request.user, 'instructor'):
        messages.info(request, "You are already an instructor")
        return redirect('instructor_dashboard')
    
    if request.method == 'POST':
        bio = request.POST.get('bio')
        specialization = request.POST.get('specialization')
        
        try:
            instructor = Instructor.objects.create(
                user=request.user,
                bio=bio,
                specialization=specialization
            )
            messages.success(request, "Congratulations! You are now an instructor")
            return redirect('instructor_dashboard')
        except Exception as e:
            messages.error(request, f"Error creating instructor profile: {str(e)}")
    
    return render(request, 'instructors/become_instructor.html')