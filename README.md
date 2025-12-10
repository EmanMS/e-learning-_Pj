# 🎓 E-Learning Platform

A comprehensive Django-based e-learning platform that enables instructors to create and manage courses while providing students with an interactive learning experience.

![Django](https://img.shields.io/badge/Django-5.2.8-green.svg)
![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Table of Contents

- [Features](#-features)
- [Technology Stack](#-technology-stack)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [API Endpoints](#-api-endpoints)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

### 👥 User Management
- **Multi-Role Authentication System**
  - Student accounts with course enrollment capabilities
  - Instructor accounts with course creation privileges
  - Admin accounts with full platform management
- **Custom User Model** with role-based permissions
- **User Profiles** with personal information management
- Secure authentication and authorization

### 📚 Course Management
- **Course Creation & Editing**
  - Rich course descriptions
  - Course thumbnails and media support
  - Category-based organization
  - Pricing options (free and paid courses)
  - Featured courses highlighting
- **Lesson Management**
  - Ordered lesson structure
  - Video content integration
  - Text-based content support
  - Duration tracking
- **Course Discovery**
  - Browse all available courses
  - Category filtering
  - Featured courses section
  - Search functionality

### 🎯 Student Features
- **Course Enrollment**
  - Easy one-click enrollment
  - Access to enrolled courses dashboard
  - Course progress tracking
- **Learning Progress**
  - Lesson completion tracking
  - Progress percentage calculation
  - Visual progress indicators
  - Completion timestamps
- **My Courses Dashboard**
  - View all enrolled courses
  - Track learning progress
  - Quick access to continue learning

### 👨‍🏫 Instructor Features
- **Instructor Dashboard**
  - Overview of created courses
  - Student enrollment statistics
  - Total students across all courses
- **Course Management**
  - Create new courses
  - Edit existing courses
  - Manage course content
  - Upload course materials
- **Instructor Profiles**
  - Bio and specialization
  - Profile pictures
  - Social media links (Website, LinkedIn)
  - Approval system for new instructors

### 🔧 Admin Features
- **Admin Dashboard**
  - Platform-wide statistics
  - Total courses, students, and instructors overview
  - Recent enrollments tracking
- **Course Management**
  - Create, edit, and delete any course
  - Manage course visibility and featured status
  - Assign courses to instructors
- **User Management**
  - Manage instructors and students
  - Approve/reject instructor applications
  - View user statistics and activity
- **Instructor Management**
  - Approve new instructor applications
  - Manage instructor permissions
  - View instructor performance

### 📊 Progress Tracking
- **Lesson Progress System**
  - Track individual lesson completion
  - Automatic progress calculation
  - Completion timestamps
  - Unique student-lesson tracking
- **Course Progress**
  - Overall course completion percentage
  - Visual progress bars
  - Completed vs. total lessons count

### 💳 Payment Integration (Ready)
- **PayPal Integration** support structure
- **Stripe Integration** support structure
- Paid and free course options
- Secure payment processing infrastructure

### 🎨 User Interface
- **Responsive Design**
  - Mobile-friendly interface
  - Tablet and desktop optimized
  - Modern, clean UI
- **Interactive Elements**
  - Dynamic course cards
  - Progress indicators
  - User-friendly navigation
  - Intuitive dashboards

## 🛠️ Technology Stack

### Backend
- **Django 5.2.8** - Web framework
- **Python 3.x** - Programming language
- **SQLite** - Database (development)
- **Django REST Framework 3.16.1** - API development
- **Django CORS Headers 4.9.0** - Cross-origin resource sharing

### Authentication & Security
- **Django Simple JWT 5.5.1** - JWT authentication
- **cryptography 46.0.3** - Encryption utilities
- **pyOpenSSL 25.3.0** - SSL/TLS support

### Media & Storage
- **Pillow 12.0.0** - Image processing
- **Cloudinary 1.44.1** - Cloud media storage
- **django-cloudinary-storage 0.3.0** - Cloudinary integration

### Payment Processing
- **PayPal REST SDK 1.13.3** - PayPal integration
- **Stripe 14.0.1** - Stripe payment processing

### Utilities
- **python-dotenv 1.2.1** - Environment variable management
- **ReportLab 4.4.5** - PDF generation
- **Requests 2.32.5** - HTTP library

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Step-by-Step Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd elearning_platform
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Apply database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a superuser (admin)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Open your browser and navigate to: `http://localhost:8000`
   - Admin panel: `http://localhost:8000/admin`

## ⚙️ Configuration

### Environment Variables
Create a `.env` file in the project root with the following variables:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (if using PostgreSQL)
DB_NAME=elearning_db
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432

# Cloudinary (for media storage)
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

# PayPal
PAYPAL_CLIENT_ID=your_paypal_client_id
PAYPAL_CLIENT_SECRET=your_paypal_client_secret
PAYPAL_MODE=sandbox  # or 'live' for production

# Stripe
STRIPE_PUBLIC_KEY=your_stripe_public_key
STRIPE_SECRET_KEY=your_stripe_secret_key
```

### Media Files
The platform supports media file uploads for:
- Course thumbnails (`course_thumbnails/`)
- Instructor profile pictures (`instructors/`)

Media files are stored in the `media/` directory by default.

## 🚀 Usage

### For Students

1. **Sign Up**
   - Navigate to the signup page
   - Select "Student" as your role
   - Complete the registration form

2. **Browse Courses**
   - View all available courses on the home page
   - Filter by category
   - Check featured courses

3. **Enroll in a Course**
   - Click on a course to view details
   - Click "Enroll Now" button
   - Access course content immediately

4. **Track Your Progress**
   - Mark lessons as complete
   - View your progress percentage
   - Access "My Courses" dashboard

### For Instructors

1. **Become an Instructor**
   - Sign up or log in
   - Navigate to "Become an Instructor"
   - Fill out the instructor application form
   - Wait for admin approval

2. **Create a Course**
   - Access the instructor dashboard
   - Click "Create New Course"
   - Fill in course details
   - Add lessons and content
   - Publish the course

3. **Manage Your Courses**
   - View all your courses in the dashboard
   - Edit course content and details
   - Track student enrollments
   - Monitor course performance

### For Administrators

1. **Access Admin Dashboard**
   - Log in with admin credentials
   - Navigate to `/admin/dashboard`

2. **Manage Courses**
   - Create, edit, or delete any course
   - Set featured courses
   - Manage course visibility

3. **Manage Users**
   - Approve instructor applications
   - View student and instructor lists
   - Manage user permissions

4. **Monitor Platform**
   - View platform statistics
   - Track enrollments
   - Monitor course activity

## 📁 Project Structure

```
elearning_platform/
├── courses/                    # Main application
│   ├── migrations/            # Database migrations
│   ├── templates/             # HTML templates
│   │   ├── courses/          # Course-related templates
│   │   └── base.html         # Base template
│   ├── templatetags/         # Custom template tags
│   ├── admin.py              # Admin configuration
│   ├── decorators.py         # Custom decorators
│   ├── forms.py              # Form definitions
│   ├── models.py             # Database models
│   ├── permissions.py        # Permission classes
│   ├── urls.py               # URL routing
│   └── views.py              # View functions
├── elearning_platform/        # Project settings
│   ├── settings.py           # Django settings
│   ├── urls.py               # Main URL configuration
│   ├── views.py              # Project-level views
│   └── wsgi.py               # WSGI configuration
├── media/                     # User-uploaded files
│   ├── course_thumbnails/    # Course images
│   └── instructors/          # Instructor photos
├── db.sqlite3                # SQLite database
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## 🔌 API Endpoints

### Authentication
- `POST /signup/` - User registration
- `POST /login/` - User login
- `POST /logout/` - User logout

### Courses
- `GET /` - Home page with course list
- `GET /course/<id>/` - Course detail page
- `POST /course/<id>/enroll/` - Enroll in a course
- `GET /my-courses/` - Student's enrolled courses

### Instructor
- `GET /instructor/dashboard/` - Instructor dashboard
- `GET /instructor/<id>/` - Instructor profile
- `POST /instructor/course/create/` - Create new course
- `POST /instructor/course/<id>/edit/` - Edit course
- `POST /become-instructor/` - Apply to become instructor

### Admin
- `GET /admin/dashboard/` - Admin dashboard
- `POST /admin/course/create/` - Admin create course
- `POST /admin/course/<id>/edit/` - Admin edit course
- `POST /admin/course/<id>/delete/` - Admin delete course
- `GET /admin/instructors/` - Manage instructors
- `GET /admin/students/` - Manage students

### Progress
- `POST /lesson/<id>/complete/` - Mark lesson as complete

## 🗄️ Database Models

### CustomUser
- Extended Django User model
- Fields: username, email, password, role, phone_number
- Roles: Student, Instructor, Admin

### Instructor
- One-to-One with CustomUser
- Fields: bio, specialization, profile_picture, website, linkedin, is_approved

### Student
- One-to-One with CustomUser
- Many-to-Many with Course (enrolled_courses)

### Course
- Fields: title, description, instructor, price, is_paid, thumbnail, category, is_active, is_featured
- Foreign Key to Instructor

### Lesson
- Fields: course, title, content, video_url, order, duration
- Foreign Key to Course

### LessonProgress
- Tracks student progress on lessons
- Fields: student, lesson, completed, completed_at
- Unique together: student + lesson

### Enrollment
- Tracks course enrollments
- Fields: student, course, enrolled_at
- Unique together: student + course

### UserProfile
- Extended user information
- Fields: user, phone_number, date_of_birth, address

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**EmanMS**

## 🙏 Acknowledgments

- Django Documentation
- Django REST Framework
- All contributors and users of this platform

## 📞 Support

For support, please open an issue in the repository or contact the development team.

---

**Note**: This platform is under active development. Features and documentation may change.
