from django.core.management.base import BaseCommand
from app2.models import Department, Semester, Subject
 
 
class Command(BaseCommand):
    help = "Bulk upload subjects for CSE and ECE department"
   
 
 
    def handle(self, *args, **kwargs):
 
        DATA = {
            "CSE": {
                1: [
                    "Engineering Mathematics I",
                    "Engineering Physics",
                    "Programming in C",
                    "Basic Electrical Engineering",
                    "Engineering Graphics",
                    "Communication Skills",
                ],
                2: [
                    "Engineering Mathematics II",
                    "Engineering Chemistry",
                    "Data Structures",
                    "Digital Electronics",
                    "Environmental Studies",
                ],
                3: [
                    "Discrete Mathematics",
                    "Object Oriented Programming",
                    "Computer Organization",
                    "Operating Systems",
                    "Data Structures Lab",
                ],
                4: [
                    "Design & Analysis of Algorithms",
                    "Database Management Systems",
                    "Software Engineering",
                    "Microprocessors",
                    "DBMS Lab",
                ],
                5: [
                    "Computer Networks",
                    "Web Technologies",
                    "Theory of Computation",
                    "Artificial Intelligence",
                    "CN Lab",
                ],
                6: [
                    "Compiler Design",
                    "Machine Learning",
                    "Cloud Computing",
                    "Cyber Security",
                    "Mini Project",
                ],
                7: [
                    "Big Data Analytics",
                    "Internet of Things",
                    "Elective I",
                    "Elective II",
                    "Project Phase I",
                ],
                8: [
                    "Elective III",
                    "Elective IV",
                    "Internship",
                    "Project Phase II",
                ],
            },
            "MECH": {
    1: [
        "Engineering Mathematics I",
        "Engineering Physics",
        "Basic Electrical Engineering",
        "Engineering Graphics",
        "Communication Skills",
    ],
    2: [
        "Engineering Mathematics II",
        "Engineering Chemistry",
        "Engineering Mechanics",
        "Programming in C",
        "Environmental Studies",
    ],
    3: [
        "Strength of Materials",
        "Manufacturing Processes",
        "Thermodynamics I",
        "Material Science",
        "Workshop Practice",
    ],
    4: [
        "Theory of Machines",
        "Fluid Mechanics",
        "Thermodynamics II",
        "Metrology & Measurements",
        "Manufacturing Technology Lab",
    ],
    5: [
        "Design of Machine Elements",
        "Heat Transfer",
        "CNC Machines",
        "Dynamics of Machines",
        "Heat Transfer Lab",
    ],
    6: [
        "Finite Element Analysis",
        "Refrigeration & Air Conditioning",
        "Automobile Engineering",
        "Mechatronics",
        "Mini Project",
    ],
    7: [
        "CAD / CAM",
        "Robotics",
        "Elective I",
        "Elective II",
        "Project Phase I",
    ],
    8: [
        "Elective III",
        "Internship",
        "Project Phase II",
    ],
},
"EEE": {
    1: [
        "Engineering Mathematics I",
        "Engineering Physics",
        "Basic Electrical Engineering",
        "Engineering Graphics",
        "Communication Skills",
    ],
    2: [
        "Engineering Mathematics II",
        "Engineering Chemistry",
        "Electronic Devices",
        "Programming in C",
        "Environmental Studies",
    ],
    3: [
        "Electrical Circuits",
        "Control Systems I",
        "Electrical Machines I",
        "Power Systems I",
        "Electrical Circuits Lab",
    ],
    4: [
        "Power Electronics",
        "Electrical Machines II",
        "Measurements & Instrumentation",
        "Control Systems II",
        "Machines Lab",
    ],
    5: [
        "Power Systems II",
        "Digital Signal Processing",
        "Microcontrollers",
        "Renewable Energy Systems",
        "DSP Lab",
    ],
    6: [
        "High Voltage Engineering",
        "Smart Grid Technology",
        "FACTS Controllers",
        "Industrial Drives",
        "Mini Project",
    ],
    7: [
        "Electric Vehicles",
        "Power Quality",
        "Elective I",
        "Elective II",
        "Project Phase I",
    ],
    8: [
        "Elective III",
        "Internship",
        "Project Phase II",
    ],
},
"CIVIL": {
    1: [
        "Engineering Mathematics I",
        "Engineering Physics",
        "Basic Civil Engineering",
        "Engineering Graphics",
        "Communication Skills",
    ],
    2: [
        "Engineering Mathematics II",
        "Engineering Chemistry",
        "Programming in C",
        "Environmental Studies",
        "Surveying I",
    ],
    3: [
        "Strength of Materials",
        "Structural Analysis I",
        "Building Materials",
        "Fluid Mechanics",
        "Surveying II",
    ],
    4: [
        "Structural Analysis II",
        "Geotechnical Engineering I",
        "Concrete Technology",
        "Hydrology",
        "Material Testing Lab",
    ],
    5: [
        "Design of RCC Structures",
        "Geotechnical Engineering II",
        "Transportation Engineering I",
        "Environmental Engineering I",
        "Survey Lab",
    ],
    6: [
        "Steel Structure Design",
        "Transportation Engineering II",
        "Environmental Engineering II",
        "Construction Planning & Management",
        "Mini Project",
    ],
    7: [
        "Advanced Foundation Engineering",
        "Disaster Management",
        "Elective I",
        "Elective II",
        "Project Phase I",
    ],
    8: [
        "Elective III",
        "Internship",
        "Project Phase II",
    ],
},
"AI": {
    1: [
        "Engineering Mathematics I",
        "Engineering Physics",
        "Programming in Python",
        "Basic Electrical Engineering",
        "Communication Skills",
    ],
    2: [
        "Engineering Mathematics II",
        "Engineering Chemistry",
        "Data Structures",
        "Digital Electronics",
        "Environmental Studies",
    ],
    3: [
        "Discrete Mathematics",
        "Object Oriented Programming",
        "Database Management Systems",
        "Computer Organization",
        "Python Lab",
    ],
    4: [
        "Artificial Intelligence",
        "Operating Systems",
        "Design & Analysis of Algorithms",
        "Probability & Statistics",
        "AI Lab",
    ],
    5: [
        "Machine Learning",
        "Data Mining",
        "Internet of Things",
        "Computer Networks",
        "ML Lab",
    ],
    6: [
        "Deep Learning",
        "Natural Language Processing",
        "Cloud Computing",
        "Cyber Security",
        "Mini Project",
    ],
    7: [
        "Computer Vision",
        "Big Data Analytics",
        "Elective I",
        "Elective II",
        "Project Phase I",
    ],
    8: [
        "Elective III",
        "Internship",
        "Project Phase II",
    ],
},
 
 
            "ECE": {
                1: [
                    "Engineering Mathematics I",
                    "Engineering Physics",
                    "Basic Electrical Engineering",
                    "Engineering Graphics",
                    "Communication Skills",
                ],
                2: [
                    "Engineering Mathematics II",
                    "Engineering Chemistry",
                    "Electronic Devices",
                    "Programming in C",
                    "Environmental Studies",
                ],
                3: [
                    "Signals & Systems",
                    "Network Theory",
                    "Digital Electronics",
                    "Analog Circuits",
                    "Digital Lab",
                ],
                4: [
                    "Control Systems",
                    "Microprocessors",
                    "Communication Theory",
                    "Linear Integrated Circuits",
                    "Microprocessor Lab",
                ],
                5: [
                    "Analog Communication",
                    "Digital Communication",
                    "VLSI Design",
                    "Embedded Systems",
                    "Communication Lab",
                ],
                6: [
                    "Microwave Engineering",
                    "Antenna & Wave Propagation",
                    "Optical Communication",
                    "IoT Systems",
                    "Mini Project",
                ],
                7: [
                    "Wireless Communication",
                    "Robotics",
                    "Elective I",
                    "Elective II",
                    "Project Phase I",
                ],
                8: [
                    "Elective III",
                    "Internship",
                    "Project Phase II",
                ],
            },
        }
 
       
        semester_map = {}

        for sem in range(1, 9):
            semester, _ = Semester.objects.get_or_create(
                sem_name=f"Semester {sem}",
                year=(1 if sem <= 2 else 2 if sem <= 4 else 3 if sem <= 6 else 4)
            )
            semester_map[sem] = semester

        
        for dept_name, semesters in DATA.items():
            try:
                department = Department.objects.get(dept_name=dept_name)
            except Department.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f"❌ Department '{dept_name}' not found")
                )
                continue

            for sem_no, subjects in semesters.items():
                semester = semester_map[sem_no]

                for subject in subjects:
                    Subject.objects.get_or_create(
                        subject_name=subject,
                        department=department,
                        semester=semester,
                        defaults={"credits": 3}
                    )

        self.stdout.write(
            self.style.SUCCESS("✅ All subjects uploaded successfully!")
        )