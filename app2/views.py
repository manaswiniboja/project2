from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4 

from app2.models import (
    Student, College, Department,
    Semester, Subject, Mark
)

PASS_MARK = 24   # Minimum marks to pass


# ================= HOME =================
def home(request):
    colleges = College.objects.all()
    departments = Department.objects.all()
    students = Student.objects.select_related('college', 'department')

    error = None
    current_year = date.today().year

    if request.method == "POST" and "student_name" in request.POST:
        sname = request.POST.get("student_name")
        sage = int(request.POST.get("student_age"))
        college_id = request.POST.get("college")
        dept_id = request.POST.get("department")
        simg = request.FILES.get("student_image")
        joined_year = int(request.POST.get("joined_year"))

        if sage < 16:
            error = "Student age must be greater than 16"
        else:
            Student.objects.create(
                sname=sname,
                sage=sage,
                joined_year=joined_year,
                college=College.objects.get(cid=college_id),
                department=Department.objects.get(did=dept_id),
                photo=simg
            )
            return redirect("home")

    return render(request, "app/home.html", {
        "colleges": colleges,
        "departments": departments,
        "students": students,
        "error": error,
        "current_year": current_year
    })


# ================= COMPLETED SEMESTERS =================
def calculate_completed_semesters(joined_year):
    today = date.today()
    years_passed = today.year - joined_year

    if today.month >= 6:
        completed = years_passed * 2
    else:
        completed = (years_passed * 2) - 1

    return max(0, min(completed, 8))


# ================= GRADE POINT =================
def get_grade_point(marks):
    if marks >= 90: return 10
    if marks >= 80: return 9
    if marks >= 70: return 8
    if marks >= 60: return 7
    if marks >= 50: return 6
    if marks >= 40: return 5
    return 0


# ================= STUDENT PROFILE =================
def student_profile(request, student_id):
    student = get_object_or_404(Student, sid=student_id)
    colleges = College.objects.all()
    departments = Department.objects.all()
    completed_semesters = calculate_completed_semesters(student.joined_year)
    semesters = Semester.objects.all().order_by("year", "sem_name")

    # Map existing marks: subject_id -> marks
    marks_map = {m.subject_id: m.marks for m in Mark.objects.filter(student=student)}

    semester_subjects = []

    # CGPA calculation
    total_points = 0
    subjects_with_marks_count = 0

    for sem_index, sem in enumerate(semesters, start=1):

        subjects = Subject.objects.filter(
            department=student.department,
            semester=sem
        ).order_by("subject_id")

        subjects_with_marks = []

        # Semester GPA calculation
        sem_total_points = 0
        sem_total_credits = 0

        for sub in subjects:
            marks = marks_map.get(sub.subject_id)
            earned_credits = 0
            gp = 0

            if marks is not None and sem_index <= completed_semesters:
                gp = get_grade_point(marks)

                # GPA calculation (credit weighted)
                sem_total_points += gp * sub.credits
                sem_total_credits += sub.credits

                # CGPA calculation
                total_points += gp
                subjects_with_marks_count += 1

                # Earned credits only if pass
                if marks >= PASS_MARK:
                    earned_credits = sub.credits

            subjects_with_marks.append({
                "subject": sub,
                "marks": marks if sem_index <= completed_semesters else None,
                "earned_credits": earned_credits,
                "grade_point": gp
            })

        semester_gpa = round(
            sem_total_points / sem_total_credits, 2
        ) if sem_total_credits else None

        semester_subjects.append({
            "semester": sem,
            "subjects": subjects_with_marks,
            "is_completed": sem_index <= completed_semesters,
            "semester_gpa": semester_gpa
        })

    cgpa = round(
        total_points / subjects_with_marks_count, 2
    ) if subjects_with_marks_count else 0.00

    return render(request, "app/student_profile.html", {
        "student": student,
        "colleges": colleges,
        "departments": departments,
        "semester_subjects": semester_subjects,
        "completed_semesters": completed_semesters,
        "total_credits": sum(
            sub['earned_credits']
            for sem in semester_subjects
            for sub in sem['subjects']
        ),
        "cgpa": cgpa
    })


# ================= SAVE SEMESTER MARKS =================
def save_semester_marks(request, student_id, semester_id):
    student = get_object_or_404(Student, sid=student_id)
    semester = get_object_or_404(Semester, sem_id=semester_id)

    if request.method == "POST":
        subjects = Subject.objects.filter(
            department=student.department,
            semester=semester
        )

        for sub in subjects:
            value = request.POST.get(f"mark_{sub.subject_id}")
            if value not in (None, ""):
                mark_obj, _ = Mark.objects.get_or_create(
                    student=student,
                    subject=sub
                )
                mark_obj.marks = int(value)
                mark_obj.save()

        messages.success(
            request,
            f"Marks for {semester.sem_name} saved successfully!"
        )

    return redirect("student_profile", student_id=student.sid)


# ================= PDF EXPORT (SEMESTER WISE WITH GPA) =================
def export_student_pdf(request, student_id):
    student = get_object_or_404(Student, sid=student_id)

    semesters = Semester.objects.all().order_by("year", "sem_name")
    marks = Mark.objects.filter(student=student).select_related("subject")
    marks_map = {m.subject_id: m.marks for m in marks}

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = (
        f'attachment; filename="{student.sname}_Academic_Report.pdf"'
    )

    doc = SimpleDocTemplate(response, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    # ---------- HEADER ----------
    elements.append(Paragraph("<b>Student Academic Report</b>", styles["Title"]))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph(f"<b>Name:</b> {student.sname}", styles["Normal"]))
    elements.append(Paragraph(
        f"<b>College:</b> {student.college.college_name}", styles["Normal"]
    ))
    elements.append(Paragraph(
        f"<b>Department:</b> {student.department.dept_name}", styles["Normal"]
    ))
    elements.append(Spacer(1, 20))

    total_credits = 0

    # ---------- SEMESTER WISE ----------
    for sem in semesters:
        subjects = Subject.objects.filter(
            department=student.department,
            semester=sem
        )

        if not subjects.exists():
            continue

        elements.append(Paragraph(
            f"<b>{sem.sem_name} (Year {sem.year})</b>",
            styles["Heading2"]
        ))
        elements.append(Spacer(1, 8))

        table_data = [
            ["Subject", "Marks", "Credits Earned", "Result"]
        ]

        sem_credits = 0
        sem_total_points = 0
        sem_total_credits = 0

        for sub in subjects:
            marks = marks_map.get(sub.subject_id)

            if marks is None:
                continue

            gp = get_grade_point(marks)

            if marks >= PASS_MARK:
                earned = sub.credits
                result = "PASS"
            else:
                earned = 0
                result = "FAIL"

            sem_credits += earned
            total_credits += earned

            # GPA calculation (credit-weighted)
            sem_total_points += gp * sub.credits
            sem_total_credits += sub.credits

            table_data.append([
                sub.subject_name,
                str(marks),
                str(earned),
                result
            ])

        table = Table(table_data, colWidths=[200, 80, 100, 80])
        elements.append(table)
        elements.append(Spacer(1, 6))

        semester_gpa = round(
            sem_total_points / sem_total_credits, 2
        ) if sem_total_credits else 0.00

        elements.append(
            Paragraph(
                f"<b>Semester Credits Earned:</b> {sem_credits}",
                styles["Normal"]
            )
        )
        elements.append(
            Paragraph(
                f"<b>Semester GPA:</b> {semester_gpa}",
                styles["Normal"]
            )
        )
        elements.append(Spacer(1, 18))

    # ---------- FINAL SUMMARY ----------
    final_result = "PASS" if total_credits >= 35 else "FAIL"

    elements.append(Spacer(1, 20))
    elements.append(Paragraph("<b>Final Summary</b>", styles["Heading2"]))
    elements.append(
        Paragraph(f"<b>Total Credits Earned:</b> {total_credits}", styles["Normal"])
    )
    elements.append(
        Paragraph(f"<b>Final Result:</b> {final_result}", styles["Normal"])
    )

    doc.build(elements)
    return response


# ================= STUDENT CRUD =================
def edit_student(request, student_id):
    student = get_object_or_404(Student, sid=student_id)

    if request.method == "POST":
        student.sname = request.POST.get("student_name")
        student.sage = int(request.POST.get("student_age"))
        student.joined_year = int(request.POST.get("joined_year"))
        student.college = College.objects.get(cid=request.POST.get("college"))
        student.department = Department.objects.get(did=request.POST.get("department"))

        if request.FILES.get("student_image"):
            student.photo = request.FILES.get("student_image")

        student.save()

    return redirect("student_profile", student_id=student.sid)


def delete_student(request, student_id):
    get_object_or_404(Student, sid=student_id).delete()
    return redirect("home")


# ================= COLLEGE CRUD =================
def edit_college(request, college_id):
    college = get_object_or_404(College, cid=college_id)
    if request.method == "POST":
        college.college_name = request.POST.get("college_name")
        college.save()
    return redirect("home")


def delete_college(request, college_id):
    get_object_or_404(College, cid=college_id).delete()
    return redirect("home")


# ================= DEPARTMENT CRUD =================
def edit_department(request, dept_id):
    dept = get_object_or_404(Department, did=dept_id)
    if request.method == "POST":
        dept.dept_name = request.POST.get("department_name")
        dept.save()
    return redirect("home")


def delete_department(request, dept_id):
    get_object_or_404(Department, did=dept_id).delete()
    return redirect("home")
