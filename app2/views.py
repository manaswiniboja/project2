from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors

from app2.models import (
    Student, College, Department,
    Semester, Subject, Mark
)

PASS_MARK = 24
TOTAL_SEMESTERS = 8   # Total semesters in course


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

    return max(0, min(completed, TOTAL_SEMESTERS))


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
    all_completed = completed_semesters >= TOTAL_SEMESTERS

    semesters = Semester.objects.all().order_by("year", "sem_name")
    marks_map = {m.subject_id: m.marks for m in Mark.objects.filter(student=student)}

    semester_subjects = []
    total_credits = 0
    total_points = 0
    subjects_with_marks_count = 0

    for sem_index, sem in enumerate(semesters, start=1):
        subjects = Subject.objects.filter(department=student.department, semester=sem)

        subjects_with_marks = []
        sem_total_points = 0
        sem_total_credits = 0

        for sub in subjects:
            marks = marks_map.get(sub.subject_id)
            earned_credits = 0
            gp = 0

            if marks is not None and sem_index <= completed_semesters:
                gp = get_grade_point(marks)
                sem_total_points += gp * sub.credits
                sem_total_credits += sub.credits
                total_points += gp
                subjects_with_marks_count += 1

                if marks >= PASS_MARK:
                    earned_credits = sub.credits
                    total_credits += sub.credits

            subjects_with_marks.append({
                "subject": sub,
                "marks": marks if sem_index <= completed_semesters else None,
                "earned_credits": earned_credits,
                "grade_point": gp
            })

        semester_gpa = round(sem_total_points / sem_total_credits, 2) if sem_total_credits else None

        semester_subjects.append({
            "semester": sem,
            "subjects": subjects_with_marks,
            "is_completed": sem_index <= completed_semesters,
            "semester_gpa": semester_gpa
        })

    cgpa = round(total_points / subjects_with_marks_count, 2) if subjects_with_marks_count else None

    final_result = "PASS" if total_credits >= 35 else "FAIL" if all_completed else None

    return render(request, "app/student_profile.html", {
        "student": student,
        "colleges": colleges,
        "departments": departments,
        "semester_subjects": semester_subjects,
        "completed_semesters": completed_semesters,
        "total_credits": total_credits,
        "cgpa": cgpa,
        "final_result": final_result,
        "all_completed": all_completed
    })


# ================= SAVE SEMESTER MARKS =================
def save_semester_marks(request, student_id, semester_id):
    student = get_object_or_404(Student, sid=student_id)
    semester = get_object_or_404(Semester, sem_id=semester_id)

    if request.method == "POST":
        subjects = Subject.objects.filter(department=student.department, semester=semester)

        for sub in subjects:
            value = request.POST.get(f"mark_{sub.subject_id}")
            if value not in (None, ""):
                mark_obj, _ = Mark.objects.get_or_create(student=student, subject=sub)
                mark_obj.marks = int(value)
                mark_obj.save()

        messages.success(request, f"Marks for {semester.sem_name} saved successfully!")

    return redirect("student_profile", student_id=student.sid)


# ================= PDF EXPORT =================
def export_student_pdf(request, student_id):
    student = get_object_or_404(Student, sid=student_id)

    completed_semesters = calculate_completed_semesters(student.joined_year)
    all_completed = completed_semesters >= TOTAL_SEMESTERS

    semesters = Semester.objects.all().order_by("year", "sem_name")
    marks = Mark.objects.filter(student=student).select_related("subject")
    marks_map = {m.subject_id: m.marks for m in marks}

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{student.sname}_Academic_Report.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph(f"<b>{student.sname} - Academic Report</b>", styles["Title"]))
    elements.append(Paragraph(f"College: {student.college.college_name}", styles["Normal"]))
    elements.append(Paragraph(f"Department: {student.department.dept_name}", styles["Normal"]))
    elements.append(Spacer(1, 12))

    total_credits = 0
    total_points = 0
    subjects_with_marks_count = 0

    for sem_index, sem in enumerate(semesters, start=1):
        subjects = Subject.objects.filter(department=student.department, semester=sem)
        if not subjects.exists():
            continue

        elements.append(Spacer(1, 12))
        elements.append(Paragraph(f"<b>{sem.sem_name} (Year {sem.year})</b>", styles["Heading2"]))
        if sem_index > completed_semesters:
            elements.append(Paragraph("Upcoming Semester", styles["Normal"]))

        table_data = [["Subject", "Credits", "Marks", "Credits Earned", "Result"]]
        sem_total_points = 0
        sem_total_credits = 0

        for sub in subjects:
            marks = marks_map.get(sub.subject_id)
            earned_credits = 0
            gp = 0
            result = "TBA"

            if marks is not None and sem_index <= completed_semesters:
                gp = get_grade_point(marks)
                sem_total_points += gp * sub.credits
                sem_total_credits += sub.credits
                total_points += gp
                subjects_with_marks_count += 1

                if marks >= PASS_MARK:
                    earned_credits = sub.credits
                    total_credits += earned_credits
                    result = "PASS"
                else:
                    result = "FAIL"

            table_data.append([
                sub.subject_name,
                sub.credits,
                marks if marks is not None else "-",
                earned_credits,
                result
            ])

        semester_gpa = round(sem_total_points / sem_total_credits, 2) if sem_total_credits else None
        if semester_gpa:
            table_data.append(["", "", "", "Semester GPA", semester_gpa])

        table = Table(table_data, colWidths=[160, 60, 60, 90, 70])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#d9d9d9')),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ('ALIGN', (1,1), (-1,-1), 'CENTER'),
        ]))
        elements.append(table)

    cgpa = round(total_points / subjects_with_marks_count, 2) if subjects_with_marks_count else None
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"<b>Total Credits Earned:</b> {total_credits}", styles["Normal"]))

    if all_completed:
        final_result = "PASS" if total_credits >= 35 else "FAIL"
        result_color = "green" if final_result == "PASS" else "red"
        elements.append(Paragraph(f"<b>Final Result:</b> <font color='{result_color}'>{final_result}</font>", styles["Normal"]))
    else:
        elements.append(Paragraph("<b>Final Result:</b> RESULT PENDING", styles["Normal"]))

    elements.append(Paragraph(f"<b>CGPA:</b> {cgpa if cgpa else 'N/A'}", styles["Normal"]))

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
