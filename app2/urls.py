from django.urls import path
from app2 import views

urlpatterns = [
    path('', views.home, name='home'),
    
    # Student CRUD
    path('student/<int:student_id>/', views.student_profile, name='student_profile'),
    path('student/edit/<int:student_id>/', views.edit_student, name='edit_student'),
    path('student/delete/<int:student_id>/', views.delete_student, name='delete_student'),

    # College CRUD
    path('college/edit/<int:college_id>/', views.edit_college, name='edit_college'),
    path('college/delete/<int:college_id>/', views.delete_college, name='delete_college'),

    # Department CRUD
    path('department/edit/<int:dept_id>/', views.edit_department, name='edit_department'),
    path('department/delete/<int:dept_id>/', views.delete_department, name='delete_department'),

   
    path('student/<int:student_id>/semester/<int:semester_id>/save/', 
         views.save_semester_marks, name='save_semester_marks'),
   
]


