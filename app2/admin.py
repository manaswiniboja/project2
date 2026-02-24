from django.contrib import admin
from .models import College, Department, Semester, Student, Subject

# College Admin
@admin.register(College)
class CollegeAdmin(admin.ModelAdmin):
    list_display = ('cid', 'college_name')
    search_fields = ('college_name',)

# Department Admin
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('did', 'dept_name')
    search_fields = ('dept_name',)

# Semester Admin
@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('sem_id', 'sem_name', 'year')
    list_filter = ('year',)
    search_fields = ('sem_name',)

# Student Admin
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('sid', 'sname', 'sage', 'college', 'department', 'semester', 'photo')
    list_filter = ('college', 'department', 'semester')
    search_fields = ('sname',)
    autocomplete_fields = ('college', 'department', 'semester')

# Subject Admin
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('subject_id', 'subject_name', 'department', 'semester', 'credits')
    list_filter = ('department', 'semester')
    search_fields = ('subject_name',)
    autocomplete_fields = ('department', 'semester')
