# Student ERP System - Project Documentation

## 1. Project Overview

**Student ERP** (Enterprise Resource Planning) is a comprehensive web-based application designed to manage student, course, and attendance information in an educational institution. It provides a centralized platform for teachers, students, and administrators to manage academic records, track attendance, and view grades.

### Key Purpose:
- Simplify attendance management
- Track student performance
- Manage course information
- Provide role-based access (Teacher, Student, Admin)

---

## 2. Technology Stack

### Backend:
- **Framework**: Django 6.0.4 (Python Web Framework)
- **Database**: SQLite3
- **Authentication**: Django Built-in Authentication System
- **Server**: Django Development Server

### Frontend:
- **HTML5** for structure
- **CSS3** (Bootstrap 5.3.0) for styling
- **JavaScript** for interactivity
- **FontAwesome Icons** for UI elements

### Key Libraries:
- `django-crispy-forms` (v2.6) - Form handling and validation
- `crispy-bootstrap5` (v2026.3) - Bootstrap integration
- `Pillow` (v12.2.0) - Image processing
- `sqlparse` (v0.5.5) - SQL parsing
- `asgiref` (v3.11.1) - ASGI support
- `tzdata` (v2026.1) - Timezone data

---

## 3. System Architecture

### Architecture Pattern: **MTV (Model-Template-View)**
```
┌─────────────────────────────────────────────┐
│         Django Application                  │
├─────────────────────────────────────────────┤
│  Models (Database Schema)                   │
│  ├── User (Custom AbstractUser)             │
│  ├── Student                                │
│  ├── Course                                 │
│  ├── Grade                                  │
│  └── Attendance                             │
├─────────────────────────────────────────────┤
│  Views (Business Logic)                     │
│  ├── Dashboard                              │
│  ├── Login/Register                         │
│  ├── Profile Management                     │
│  ├── Attendance Management                  │
│  ├── Grade Management                       │
│  └── Course Management                      │
├─────────────────────────────────────────────┤
│  Templates (HTML/UI)                        │
│  ├── base.html (Layout)                     │
│  ├── accounts/ (Auth Pages)                 │
│  ├── attendance/ (Attendance Pages)         │
│  └── grades/ (Grade Pages)                  │
└─────────────────────────────────────────────┘
```

---

## 4. Core Components & Modules

### 4.1 Authentication Module (`accounts/`)
**Purpose**: User authentication and authorization

**Components:**
- **User Model**: Custom AbstractUser with roles (admin, teacher, student)
- **Views**:
  - `dashboard()` - Landing page for authenticated users
  - `profile()` - View user profile
  - `edit_profile()` - Edit profile information
  - Login/Logout (Django built-in)
- **Features**:
  - Role-based access control
  - Secure password hashing
  - Session management
  - CSRF protection on all forms

### 4.2 Students Module (`students/`)
**Purpose**: Manage student information and enrollment

**Components:**
- **Student Model**: 
  - OneToOne relationship with User
  - ManyToMany relationship with Course (enrollment)
  - Fields: user, student_id, courses
- **Features**:
  - Unique student ID
  - Course enrollment tracking
  - Profile management

### 4.3 Courses Module (`courses/`)
**Purpose**: Manage course information and teacher assignments

**Components:**
- **Course Model**:
  - Fields: code, name, credits, department, teacher
  - Foreign key to User (Teacher)
- **Features**:
  - Course code and name
  - Credit hours
  - Department classification
  - Teacher assignment
- **Security**: Only assigned teachers can manage their courses

### 4.4 Attendance Module (`attendance/`) ⭐ **KEY FEATURE**
**Purpose**: Track student attendance by course and date

**Components:**
- **Attendance Model**:
  - Foreign key to Student
  - Foreign key to Course
  - Date field
  - Status choices: Present, Absent, Late, Excused
  - Remarks field
  - Tracked by (marked_by teacher)
  - Unique constraint on (student, course, date)

**Views:**
- `attendance_list()` - View attendance records
  - Teachers see all records
  - Students see only their records
- `mark_attendance()` - Mark attendance (POST request)
  - Teachers select course and date
  - Mark status for each enrolled student
  - Add optional remarks
  - Save with timestamp

**Features:**
- Course-based attendance marking
- Student enrollment checking
- Remarks/notes for each record
- Prevents duplicate entries
- Role-based data filtering

### 4.5 Grades Module (`grades/`)
**Purpose**: Manage student grades

**Components:**
- **Grade Model**: Student grade tracking
- Uses: ForeignKey to Student, Course, Grade value
- **Features**: Grade calculation and tracking

---

## 5. Database Schema

### Entity Relationship Diagram:
```
User (accounts_user)
├── role (ENUM: admin, teacher, student)
├── username, email, password
├── first_name, last_name
└── is_active, is_staff

Student (students_student)
├── user_id (OneToOne → User)
├── student_id (Unique)
└── courses (ManyToMany → Course)

Course (courses_course)
├── code (Unique)
├── name, credits, department
├── teacher_id (ForeignKey → User)
└── students (ManyToMany → Student)

Attendance (attendance_attendance)
├── student_id (ForeignKey → Student)
├── course_id (ForeignKey → Course)
├── date
├── status (ENUM: present, absent, late, excused)
├── remarks
├── marked_by_id (ForeignKey → User)
└── Unique(student, course, date)

Grade (grades_grade)
├── student_id (ForeignKey → Student)
├── course_id (ForeignKey → Course)
├── grade (Decimal)
└── Unique(student, course)
```

---

## 6. User Roles & Permissions

### 6.1 **Student Role**
**Permissions:**
- ✅ View own profile
- ✅ View own attendance records
- ✅ View own grades
- ✅ Edit own profile
- ❌ Mark attendance
- ❌ View other students' data

**Workflow:**
1. Login
2. View dashboard
3. Check attendance history
4. View grades
5. Edit profile

### 6.2 **Teacher Role**
**Permissions:**
- ✅ View all attendance records
- ✅ Mark attendance for own courses
- ✅ View student information
- ✅ View grades
- ✅ Manage grades
- ❌ Access admin panel (without admin role)

**Workflow:**
1. Login
2. View dashboard
3. Mark attendance (select course → select date → mark students)
4. View attendance records
5. Manage grades

### 6.3 **Admin Role**
**Permissions:**
- ✅ Access Django admin panel
- ✅ Manage all users (create, edit, delete)
- ✅ Manage courses
- ✅ Manage students
- ✅ View all records
- ✅ Create/modify student and course data

---

## 7. Key Features Explanation

### 7.1 Attendance Management System

**Flow Diagram:**
```
Teacher Login
    ↓
Navigate to Attendance → Mark Attendance
    ↓
Select Course from dropdown
    ↓
Select Date
    ↓
System fetches students enrolled in course
    ↓
Teacher marks each student (Present/Absent/Late/Excused)
    ↓
Optional: Add remarks
    ↓
Submit Form (POST request)
    ↓
Django processes form data
    ↓
For each student:
   - Check if attendance exists for that date
   - Create or Update attendance record
   - Save teacher who marked it
    ↓
Redirect to attendance list
    ↓
Success message shown
```

**Why POST instead of GET (405 Error Fix):**
- Security: Django 6.0 requires POST for state-changing operations
- CSRF Protection: Prevents cross-site attacks
- Best Practice: GET for retrieving data, POST for creating/updating

### 7.2 Role-Based Data Filtering

**Students Viewing Attendance:**
```python
# Query: Get only current student's attendance
Attendance.objects.filter(student=current_student)
```

**Teachers Viewing Attendance:**
```python
# Query: Get all attendance records
Attendance.objects.all()
```

### 7.3 Data Validation

**Unique Constraint Example:**
```
Attendance Model:
- unique_together = ['student', 'course', 'date']

Prevents: Duplicate attendance marking
- Same student can't have multiple entries for same course on same date
- Ensures data integrity
```

---

## 8. Project Structure

```
student_erp/
├── core/                 # Main project settings
│   ├── settings.py      # Configuration (INSTALLED_APPS, databases, middleware)
│   ├── urls.py          # Main URL routing
│   ├── asgi.py          # ASGI configuration
│   └── wsgi.py          # WSGI configuration
│
├── accounts/            # User authentication & management
│   ├── models.py        # User model
│   ├── views.py         # Login, register, profile views
│   ├── urls.py          # Account routes
│   ├── admin.py         # Django admin configuration
│   └── management/commands/populate_data.py  # Dummy data creation
│
├── students/            # Student information
│   ├── models.py        # Student model
│   ├── views.py         # Student views
│   ├── urls.py          # Student routes
│   └── admin.py         # Admin configuration
│
├── courses/             # Course management
│   ├── models.py        # Course model
│   ├── views.py         # Course views
│   ├── urls.py          # Course routes
│   └── admin.py
│
├── attendance/          # Attendance tracking ⭐
│   ├── models.py        # Attendance model
│   ├── views.py         # Mark & view attendance
│   ├── urls.py          # Attendance routes
│   └── admin.py
│
├── grades/              # Grade management
│   ├── models.py        # Grade model
│   ├── views.py         # Grade views
│   ├── urls.py          # Grade routes
│   └── admin.py
│
├── templates/           # HTML templates
│   ├── base.html        # Base layout (navbar, sidebar)
│   ├── accounts/        # Auth templates
│   ├── attendance/      # Attendance templates
│   └── grades/          # Grade templates
│
├── static/              # CSS, JS, images
│
├── db.sqlite3           # Database file
├── manage.py            # Django management tool
├── env/                 # Virtual environment
├── tmp_logout_test.py   # Test file
└── pyvenv.cfg          # Python environment config
```

---

## 9. How Everything Works Together

### User Registration Flow:
```
1. User visits /register/
2. Sees registration form
3. Fills: username, email, password, first_name, last_name
4. Form validates input
5. User created in database with hashed password
6. User redirected to login
```

### Login Flow:
```
1. User visits /login/
2. Enters username and password
3. Django authenticates user
4. Creates session cookie
5. Redirects to dashboard based on role
6. Session maintained for subsequent requests
```

### Attendance Marking Flow (Detailed):
```
1. Teacher logs in
2. Navigates to Attendance → Mark Attendance
3. Request sent to /attendance/mark/ (GET)
4. Server fetches:
   - All courses (Course.objects.all())
   - All students (Student.objects.all())
   - Today's date
5. Renders mark.html with course dropdown
6. Teacher selects a course
7. JavaScript shows students table
8. Teacher marks each student + adds remarks
9. Teacher clicks "Save Attendance"
10. POST request sent with:
    - course_id
    - date
    - attendance_studentX (status)
    - remarks_studentX (optional)
    - csrf_token (security)
11. Django view processes POST:
    - Validates course selection
    - Gets students enrolled in course
    - For each student:
      * Extracts status from POST data
      * Extracts remarks from POST data
      * Creates/updates Attendance record
      * Links to teacher (marked_by)
12. Success message displayed
13. Redirects to /attendance/list/
```

### Attendance Viewing Flow:
```
Student Login:
1. Navigates to Attendance
2. Django checks: user.role == 'student'
3. Fetches related Student object
4. Queries: Attendance.objects.filter(student=student)
5. Shows only their records

Teacher Login:
1. Navigates to Attendance
2. Django checks: user.role != 'student'
3. Queries: Attendance.objects.all()
4. Shows all records
```

---

## 10. Security Features Implemented

### 10.1 Authentication
- **Django Authentication**: Built-in user authentication system
- **Password Hashing**: PBKDF2 algorithm (Django default)
- **Session Management**: Secure HTTP-only cookies

### 10.2 Authorization
- **Role-Based Access Control (RBAC)**:
  - Frontend: Conditional navbar based on role
  - Backend: View decorators check user role
  - Database: Queries filtered by user

### 10.3 CSRF Protection
- **CSRF Tokens**: All forms include {% csrf_token %}
- **POST Method**: Used for state-changing operations
- **Validates**: Server verifies token before processing

### 10.4 Form Validation
- **Client-side**: HTML5 validation (required, date picker)
- **Server-side**: Django form validation
- **Database**: Unique constraints prevent duplicates

### 10.5 SQL Injection Prevention
- **ORM Usage**: Django ORM prevents SQL injection
- **Parameterized Queries**: Values passed separately from SQL

---

## 11. Data Flow Diagram

```
┌──────────────┐
│   Browser    │
│ (HTML/CSS/JS)│
└──────┬───────┘
       │ HTTP Request
       ↓
┌──────────────────────┐
│   Django URL Router  │
│ (core/urls.py)       │
└──────┬───────────────┘
       │ Route Match
       ↓
┌──────────────────────┐
│   View Function      │
│ (attendance/views.py)│
└──────┬───────────────┘
       │ Query/Process
       ↓
┌──────────────────────┐
│   Models & ORM       │
│ (attendance/models)  │
└──────┬───────────────┘
       │ SQL Query
       ↓
┌──────────────────────┐
│   SQLite Database    │
│ (db.sqlite3)         │
└──────┬───────────────┘
       │ Data Result
       ↓
┌──────────────────────┐
│   Template Render    │
│ (attendance/list.html)
└──────┬───────────────┘
       │ HTML Response
       ↓
┌──────────────┐
│   Browser    │
│ Display Page │
└──────────────┘
```

---

## 12. Dummy Data Created

### Teachers (3):
- teacher1 (Dr. Kapoor) - CS courses
- teacher2 (Prof. Iyer) - CS & Math
- teacher3 (Dr. Reddy) - Math & English

### Students (8):
- STU001 - Aarav Sharma
- STU002 - Priya Patel
- STU003 - Rohan Gupta
- STU004 - Ananya Singh
- STU005 - Arjun Kumar
- STU006 - Neha Desai
- STU007 - Vikram Rao
- STU008 - Divya Nambiar

### Courses (6):
- CS101, CS201, CS301 (Computer Science)
- MATH101, MATH201 (Mathematics)
- ENG101 (English)

### Attendance:
- Sample records for last 5 days
- Various statuses (Present, Absent, Late, Excused)

---

## 13. How to Present This Project

### For Academic/Interview:

**Opening Statement:**
> "This is a Student ERP system built on Django. It's a web application that manages attendance, grades, and course information for an educational institution. The key feature is an attendance management system that allows teachers to mark attendance by course and date, while students can view their own attendance records."

**Technical Overview:**
- Django MTV architecture
- SQLite database
- Custom User model with role-based access control
- RESTful routing patterns

**Key Features:**
1. **Attendance Management**: Teachers mark attendance, students view records
2. **Role-Based Access**: Different views for students, teachers, admins
3. **Data Integrity**: Unique constraints prevent duplicate entries
4. **Security**: CSRF protection, password hashing, SQL injection prevention

**Problem Solved:**
- Manual attendance tracking → Automated digital system
- Scattered student records → Centralized database
- No attendance history → Complete historical records

**Technical Highlights:**
- Custom authentication system with roles
- ManyToMany relationships (students-courses)
- POST-based forms with CSRF tokens
- QuerySet filtering for role-based access
- Management commands for data seeding

---

## 14. Future Enhancements

1. **Attendance Reports**: Generate PDF reports, graphs, statistics
2. **Email Notifications**: Send attendance alerts to parents
3. **Mobile App**: React Native/Flutter mobile version
4. **REST API**: Expose APIs for third-party integrations
5. **Advanced Search**: Filter attendance by date range, course
6. **Export Features**: Excel/CSV export of attendance records
7. **Real-time Notifications**: WebSocket for live updates
8. **Biometric Integration**: Fingerprint/facial recognition
9. **Performance Monitoring**: Dashboard with attendance rates
10. **Schedule Management**: Class timetable integration

---

## 15. Deployment Checklist

- [ ] Set DEBUG = False in settings.py
- [ ] Set ALLOWED_HOSTS properly
- [ ] Use PostgreSQL instead of SQLite
- [ ] Use production WSGI server (Gunicorn)
- [ ] Setup SSL/HTTPS
- [ ] Configure static files collection
- [ ] Setup environment variables for secrets
- [ ] Create database backups
- [ ] Setup error logging
- [ ] Configure email backend
- [ ] Setup CDN for static files
- [ ] Load testing and optimization

---

## 16. Conclusion

The Student ERP system demonstrates:
- ✅ Full-stack Django development
- ✅ Database design and relationships
- ✅ User authentication and authorization
- ✅ Form handling and validation
- ✅ Template inheritance and styling
- ✅ Data security and protection
- ✅ Real-world problem solving

This project is a complete, working system that can manage attendance for educational institutions with proper security, data validation, and role-based access control.
