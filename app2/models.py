from datetime import datetime
from django.db import models

class College(models.Model):
    cid = models.AutoField(primary_key=True)
    college_name = models.CharField(max_length=100)

    def __str__(self):
        return self.college_name

class Department(models.Model):
    did = models.AutoField(primary_key=True)
    dept_name = models.CharField(max_length=100)

    def __str__(self):
        return self.dept_name

class Semester(models.Model):
    sem_id = models.AutoField(primary_key=True)
    sem_name = models.CharField(max_length=50)
    year = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"Year {self.year} - {self.sem_name}"

class Student(models.Model):
    sid = models.AutoField(primary_key=True)
    sname = models.CharField(max_length=100)
    sage = models.PositiveIntegerField()
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, null=True, blank=True)
    photo = models.ImageField(upload_to='students/', blank=True, null=True)
    joined_year = models.PositiveIntegerField("Joined Year")

    def __str__(self):
        return self.sname

class Subject(models.Model):
    subject_id = models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    credits = models.PositiveIntegerField()

    def __str__(self):
        return self.subject_name
    
class Mark(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks = models.PositiveIntegerField(null=True, blank=True)  

    class Meta:
        unique_together = ('student', 'subject')  

    def __str__(self):
        return f"{self.student.sname} - {self.subject.subject_name}"
    
    
from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class StudentID(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)


class FacultyID(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)  # hashed password

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.username
