from django.urls import path
from . import views

urlpatterns = [
    # المسارات الأساسية الحالية
    path('', views.home, name='home'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('enroll/<int:course_id>/', views.enroll_course, name='enroll_course'),
    path('my-courses/', views.my_courses, name='my_courses'),
    path('mark-complete/<int:lesson_id>/', views.mark_lesson_complete, name='mark_lesson_complete'),
    

     # مسارات الادمن
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/courses/create/', views.admin_course_create, name='admin_course_create'),
    path('admin/courses/<int:course_id>/edit/', views.admin_course_edit, name='admin_course_edit'),
    path('admin/courses/<int:course_id>/delete/', views.admin_course_delete, name='admin_course_delete'),
    path('admin/instructors/', views.admin_instructors, name='admin_instructors'),
    path('admin/students/', views.admin_students, name='admin_students'),

    # مسارات التسجيل والدخول
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # ========== مسارات الإنستراكتور الجديدة ==========
    path('instructor/<int:instructor_id>/', views.instructor_profile, name='instructor_profile'),
    path('instructor/dashboard/', views.instructor_dashboard, name='instructor_dashboard'),
    path('instructor/courses/create/', views.create_course, name='create_course'),
    path('instructor/courses/<int:course_id>/edit/', views.edit_course, name='edit_course'),
    path('instructor/become/', views.become_instructor, name='become_instructor'),
]