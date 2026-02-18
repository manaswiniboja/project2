from django.urls import path
from app2 import views

urlpatterns = [

    # 🔐 Authentication
    path('', views.user_login, name="login"),
    path('logout/', views.user_logout, name="logout"),
    path('faculty-register/', views.faculty_register, name="faculty_register"),
    path('student-register/', views.student_register, name="student_register"),

    # 🏠 Home (Faculty Dashboard)
    path('home/', views.home, name='home'),

    # 🎓 Student
    path('student/<int:student_id>/', views.student_profile, name='student_profile'),
    path('student/edit/<int:student_id>/', views.edit_student, name='edit_student'),
    path('student/delete/<int:student_id>/', views.delete_student, name='delete_student'),

    # 🏫 College
    path('college/edit/<int:college_id>/', views.edit_college, name='edit_college'),
    path('college/delete/<int:college_id>/', views.delete_college, name='delete_college'),

    # 🏢 Department
    path('department/edit/<int:dept_id>/', views.edit_department, name='edit_department'),
    path('department/delete/<int:dept_id>/', views.delete_department, name='delete_department'),

    # 📚 Marks
    path(
        'student/<int:student_id>/semester/<int:semester_id>/save/',
        views.save_semester_marks,
        name='save_semester_marks'
    ),

    # 📄 PDF
    path(
        'student/<int:student_id>/download-pdf/',
        views.export_student_pdf,
        name='export_student_pdf'
    ),
]
