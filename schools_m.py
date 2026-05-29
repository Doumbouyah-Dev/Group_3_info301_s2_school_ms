import json
import os
import re
from datetime import datetime

# ===========================================
# We create Class for Student, 
# ==========================================
class Student:
    def __init__(self, student_id, name, grade, dob, gender, phone):
        self.id = str(student_id)     # Unified string representations for consistent lookups
        self.name = name
        self.grade = grade          # current grade/class selected from valid list
        self.dob = dob              # validated date of birth string YYYY-MM-DD
        self.gender = gender
        self.phone = phone

    def to_list(self):
        return [self.id, self.name, self.grade, self.dob, self.gender, self.phone]

    @staticmethod
    def from_list(data):
        return Student(data[0], data[1], data[2], data[3], data[4], data[5])

class Teacher:
    def __init__(self, teacher_id, name, qualification, subjects, phone):
        self.id = str(teacher_id)
        self.name = name
        self.qualification = qualification
        self.subjects = subjects      
        self.phone = phone
        self.assigned_grades = []     

    def to_list(self):
        grades_str = ",".join(self.assigned_grades)
        return [self.id, self.name, self.qualification, self.subjects, self.phone, grades_str]

    @staticmethod
    def from_list(data):
        t = Teacher(data[0], data[1], data[2], data[3], data[4])
        if len(data) > 5 and data[5]:
            t.assigned_grades = data[5].split(",")
        else:
            t.assigned_grades = []
        return t

class Subject:
    def __init__(self, subject_id, name):
        self.id = str(subject_id)
        self.name = name
        self.assigned_grades = []    

    def to_list(self):
        grades_str = ",".join(self.assigned_grades)
        return [self.id, self.name, grades_str]

    @staticmethod
    def from_list(data):
        s = Subject(data[0], data[1])
        if len(data) > 2 and data[2]:
            s.assigned_grades = data[2].split(",")
        else:
            s.assigned_grades = []
        return s

class Grade:
    def __init__(self, grade_name, description=""):
        self.name = grade_name
        self.description = description

    def to_list(self):
        return [self.name, self.description]

    @staticmethod
    def from_list(data):
        return Grade(data[0], data[1] if len(data) > 1 else "")

class Enrollment:
    def __init__(self, student_id, grade_name, enroll_date=None):
        self.student_id = str(student_id)
        self.grade_name = grade_name
        self.enroll_date = enroll_date if enroll_date else datetime.now().strftime("%Y-%m-%d")

    def to_list(self):
        return [self.student_id, self.grade_name, self.enroll_date]

    @staticmethod
    def from_list(data):
        return Enrollment(data[0], data[1], data[2] if len(data) > 2 else None)

class Score:
    def __init__(self, student_id, subject_id, teacher_id, score, date=None):
        self.student_id = str(student_id)
        self.subject_id = str(subject_id)
        self.teacher_id = str(teacher_id) if teacher_id else ""
        self.score = score            # numeric score (0-100)
        self.date = date if date else datetime.now().strftime("%Y-%m-%d")

    def to_list(self):
        return [self.student_id, self.subject_id, self.teacher_id, str(self.score), self.date]

    @staticmethod
    def from_list(data):
        return Score(data[0], data[1], data[2], float(data[3]), data[4])

# ---------------------------- File Handling ----------------------------
class DataManager:
    FILES = {
        "students": "students.json",
        "teachers": "teachers.json",
        "subjects": "subjects.json",
        "grades": "grades.json",
        "enrollments": "enrollments.json",
        "scores": "scores.json"
    }

    @staticmethod
    def load_json(filename, obj_converter):
        data = []
        if not os.path.exists(filename):
            return data
        try:
            with open(filename, 'r', newline='', encoding='utf-8') as f:
                data = json.load(f)
                return [obj_converter(item) for item in data]
        except Exception as e:
            print(f"Error loading {filename}: {e}")
        return data

    @staticmethod
    def save_json(filename, data_list, to_list_func):
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                json.dump([to_list_func(item) for item in data_list], f)
        except Exception as e:
            print(f"Error saving {filename}: {e}")

# ---------------------------- School Management System ----------------------------
class SchoolSystem:
    # Professionally defined constants for strict field tracking
    VALID_GRADES = [f"Grade {i}" for i in range(1, 13)]

    def __init__(self):
        self.students = []          
        self.teachers = []          
        self.subjects = []          
        self.grades = []            
        self.enrollments = []       
        self.scores = []            
        self.load_all_data()

    def load_all_data(self):
        self.students = DataManager.load_json(DataManager.FILES["students"], Student.from_list)
        self.teachers = DataManager.load_json(DataManager.FILES["teachers"], Teacher.from_list)
        self.subjects = DataManager.load_json(DataManager.FILES["subjects"], Subject.from_list)
        self.grades = DataManager.load_json(DataManager.FILES["grades"], Grade.from_list)
        self.enrollments = DataManager.load_json(DataManager.FILES["enrollments"], Enrollment.from_list)
        self.scores = DataManager.load_json(DataManager.FILES["scores"], Score.from_list)

    def save_all_data(self):
        DataManager.save_json(DataManager.FILES["students"], self.students, Student.to_list)
        DataManager.save_json(DataManager.FILES["teachers"], self.teachers, Teacher.to_list)
        DataManager.save_json(DataManager.FILES["subjects"], self.subjects, Subject.to_list)
        DataManager.save_json(DataManager.FILES["grades"], self.grades, Grade.to_list)
        DataManager.save_json(DataManager.FILES["enrollments"], self.enrollments, Enrollment.to_list)
        DataManager.save_json(DataManager.FILES["scores"], self.scores, Score.to_list)

    # ------------------------ Strict Validation Helper Functions ------------------------
    def input_int_only(self, prompt):
        """Ensures the entry contains digits only (Integers)."""
        while True:
            val = input(prompt).strip()
            if val.isdigit():
                return val
            print("Invalid input. Please enter numbers (integers) only.")

    def input_human_name(self, prompt, allow_empty=False):
        """Allows only alphabetical letters and spaces for realistic human names."""
        while True:
            val = input(prompt).strip()
            if not val and allow_empty:
                return val
            if val and re.match(r"^[A-Za-z\s.\'\-]+$", val):
                return val
            print("Invalid name. Please enter text using letters only.")

    def input_dob(self, prompt, allow_empty=False):
        """Validates YYYY-MM-DD sequence with month (01-12) and day bounds (01-31)."""
        while True:
            val = input(prompt).strip()
            if not val and allow_empty:
                return val
            if re.match(r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$", val):
                return val
            print("Invalid date alignment. Format must be exactly YYYY-MM-DD (Months: 01-12, Days: 01-31).")

    def input_gender(self, prompt, allow_empty=False):
        """Enforces matching constraints for M, Male, F, or Female."""
        while True:
            val = input(prompt).strip()
            if not val and allow_empty:
                return val
            val_norm = val.strip().title()
            if val_norm in ["M", "Male"]:
                return "Male"
            elif val_norm in ["F", "Female"]:
                return "Female"
            print("Invalid response. Please enter 'M', 'Male', 'F', or 'Female'.")

    def input_grade_selection(self, prompt, allow_empty=False):
        """Presents standard choices ranging from Grade 1 to Grade 12."""
        print("\nAvailable Grades:")
        for idx, g_name in enumerate(self.VALID_GRADES, 1):
            print(f"  {idx}. {g_name}")
        while True:
            choice = input(prompt).strip()
            if not choice and allow_empty:
                return choice
            if choice.isdigit():
                idx = int(choice)
                if 1 <= idx <= len(self.VALID_GRADES):
                    return self.VALID_GRADES[idx - 1]
            print(f"Invalid choice. Please choose a number between 1 and {len(self.VALID_GRADES)}.")

    def input_phone_number(self, prompt, allow_empty=False):
        """Validates specific prefixes followed by exactly 6 more digits."""
        prefixes = ["0775", "0776", "0777", "0778", "0779", "0770", "0772", "0760", "0555", "0886", "0888", "0880"]
        pattern = f"^({'|'.join(prefixes)})\\d{{6}}$"
        while True:
            val = input(prompt).strip()
            if not val and allow_empty:
                return val
            if re.match(pattern, val):
                return val
            print("Invalid Phone Number! Must begin with a valid prefix (e.g., 0777, 0886) followed by exactly 6 digits.")

    def input_id(self, prompt, existing_ids, allow_duplicate=False):
        while True:
            id_val = self.input_int_only(prompt)
            if allow_duplicate or id_val not in existing_ids:
                return id_val
            print(f"ID '{id_val}' already exists. Please enter a unique ID.")

    def input_menu_choice(self, prompt, valid_options):
        while True:
            choice = input(prompt).strip()
            if choice in valid_options:
                return choice
            print(f"Invalid option. Please pick a number from: {', '.join(valid_options)}")

    # ------------------------ Finders ------------------------
    def find_student_by_id(self, student_id):
        for s in self.students:
            if s.id == str(student_id):
                return s
        return None

    def find_teacher_by_id(self, teacher_id):
        for t in self.teachers:
            if t.id == str(teacher_id):
                return t
        return None

    def find_subject_by_id(self, subject_id):
        for sub in self.subjects:
            if sub.id == str(subject_id):
                return sub
        return None

    def find_grade_by_name(self, grade_name):
        for g in self.grades:
            if g.name.lower() == grade_name.lower():
                return g
        return None

    # ------------------------ Student Management ------------------------
    def add_student(self):
        print("\n--- Add New Student ---")
        existing_ids = {s.id for s in self.students}
        sid = self.input_id("Student ID (Integers Only): ", existing_ids)
        name = self.input_human_name("Name (Alphabets only): ")
        grade = self.input_grade_selection("Select Current Grade option number: ")
        dob = self.input_dob("Date of Birth (YYYY-MM-DD): ")
        gender = self.input_gender("Gender (M/Male/F/Female): ")
        phone = self.input_phone_number("Phone (Valid structure only): ")
        self.students.append(Student(sid, name, grade, dob, gender, phone))
        print("Student added successfully!")

    def view_all_students(self):
        print("\n--- All Students ---")
        if not self.students:
            print("No students found.")
            return
        for s in self.students:
            print(f"ID: {s.id}, Name: {s.name}, Grade: {s.grade}, DOB: {s.dob}, Gender: {s.gender}, Phone: {s.phone}")

    def update_student(self):
        print("\n--- Update Student ---")
        sid = self.input_int_only("Enter Student ID to update: ")
        student = self.find_student_by_id(sid)
        if not student:
            print("Student not found.")
            return
        print("Leave field empty to keep current value.")
        name = self.input_human_name(f"Name ({student.name}): ", allow_empty=True)
        if name:
            student.name = name
        grade = self.input_grade_selection(f"Grade ({student.grade}) - pick new selection number: ", allow_empty=True)
        if grade:
            student.grade = grade
        dob = self.input_dob(f"Date of Birth ({student.dob}): ", allow_empty=True)
        if dob:
            student.dob = dob
        gender = self.input_gender(f"Gender ({student.gender}): ", allow_empty=True)
        if gender:
            student.gender = gender
        phone = self.input_phone_number(f"Phone ({student.phone}): ", allow_empty=True)
        if phone:
            student.phone = phone
        print("Student updated successfully!")

    def delete_student(self):
        print("\n--- Delete Student ---")
        sid = self.input_int_only("Enter Student ID to delete: ")
        student = self.find_student_by_id(sid)
        if not student:
            print("Student not found.")
            return
        confirm = self.input_menu_choice(f"Delete student {student.name} (ID: {sid})? (y/n): ", ['y', 'n', 'Y', 'N']).lower()
        if confirm == 'y':
            self.students = [s for s in self.students if s.id != sid]
            self.enrollments = [e for e in self.enrollments if e.student_id != sid]
            self.scores = [sc for sc in self.scores if sc.student_id != sid]
            print("Student deleted successfully.")
        else:
            print("Deletion cancelled.")

    def search_student(self):
        print("\n--- Search Student by ID ---")
        sid = self.input_int_only("Enter Student ID: ")
        student = self.find_student_by_id(sid)
        if student:
            print(f"Found: ID: {student.id}, Name: {student.name}, Grade: {student.grade}, DOB: {student.dob}, Gender: {student.gender}, Phone: {student.phone}")
        else:
            print("Student not found.")

    # ------------------------ Teacher Management ------------------------
    def add_teacher(self):
        print("\n--- Add New Teacher ---")
        existing_ids = {t.id for t in self.teachers}
        tid = self.input_id("Teacher ID (Integers Only): ", existing_ids)
        name = self.input_human_name("Name (Alphabets only): ")
        qualification = input("Qualification: ").strip()
        subjects = input("Subjects (comma-separated): ").strip()
        phone = self.input_phone_number("Phone (Valid structure only): ")
        self.teachers.append(Teacher(tid, name, qualification, subjects, phone))
        print("Teacher added successfully!")

    def view_all_teachers(self):
        print("\n--- All Teachers ---")
        if not self.teachers:
            print("No teachers found.")
            return
        for t in self.teachers:
            grades = ", ".join(t.assigned_grades) if t.assigned_grades else "None"
            print(f"ID: {t.id}, Name: {t.name}, Qualification: {t.qualification}, Subjects: {t.subjects}, Phone: {t.phone}, Assigned Grades: {grades}")

    def assign_teacher_to_grade(self):
        print("\n--- Assign Teacher to Grade ---")
        tid = self.input_int_only("Teacher ID: ")
        teacher = self.find_teacher_by_id(tid)
        if not teacher:
            print("Teacher not found.")
            return
        grade_name = self.input_grade_selection("Select Grade option to assign to teacher: ")
        if grade_name not in teacher.assigned_grades:
            teacher.assigned_grades.append(grade_name)
            print(f"Teacher {teacher.name} assigned to grade {grade_name}.")
        else:
            print("Teacher already assigned to this grade.")

    def update_teacher(self):
        print("\n--- Update Teacher ---")
        tid = self.input_int_only("Enter Teacher ID to update: ")
        teacher = self.find_teacher_by_id(tid)
        if not teacher:
            print("Teacher not found.")
            return
        print("Leave field empty to keep current value.")
        name = self.input_human_name(f"Name ({teacher.name}): ", allow_empty=True)
        if name:
            teacher.name = name
        qual = input(f"Qualification ({teacher.qualification}): ").strip()
        if qual:
            teacher.qualification = qual
        subjects = input(f"Subjects ({teacher.subjects}): ").strip()
        if subjects:
            teacher.subjects = subjects
        phone = self.input_phone_number(f"Phone ({teacher.phone}): ", allow_empty=True)
        if phone:
            teacher.phone = phone
        print("Teacher updated successfully!")

    def delete_teacher(self):
        print("\n--- Delete Teacher ---")
        tid = self.input_int_only("Enter Teacher ID to delete: ")
        teacher = self.find_teacher_by_id(tid)
        if not teacher:
            print("Teacher not found.")
            return
        confirm = self.input_menu_choice(f"Delete teacher {teacher.name} (ID: {tid})? (y/n): ", ['y', 'n', 'Y', 'N']).lower()
        if confirm == 'y':
            self.teachers = [t for t in self.teachers if t.id != tid]
            self.scores = [sc for sc in self.scores if sc.teacher_id != tid]
            print("Teacher deleted successfully.")
        else:
            print("Deletion cancelled.")

    # ------------------------ Subject Management ------------------------
    def add_subject(self):
        print("\n--- Add New Subject ---")
        existing_ids = {sub.id for sub in self.subjects}
        sid = self.input_id("Subject ID (Integers Only): ", existing_ids)
        name = input("Subject Name: ").strip()
        self.subjects.append(Subject(sid, name))
        print("Subject added successfully!")

    def view_all_subjects(self):
        print("\n--- All Subjects ---")
        if not self.subjects:
            print("No subjects found.")
            return
        for sub in self.subjects:
            grades = ", ".join(sub.assigned_grades) if sub.assigned_grades else "None"
            print(f"ID: {sub.id}, Name: {sub.name}, Assigned Grades: {grades}")

    def assign_subject_to_grade(self):
        print("\n--- Assign Subject to Grade ---")
        sub_id = self.input_int_only("Subject ID: ")
        subject = self.find_subject_by_id(sub_id)
        if not subject:
            print("Subject not found.")
            return
        grade_name = self.input_grade_selection("Select Grade option to assign to subject: ")
        if grade_name not in subject.assigned_grades:
            subject.assigned_grades.append(grade_name)
            print(f"Subject {subject.name} assigned to grade {grade_name}.")
        else:
            print("Subject already assigned to this grade.")

    # ------------------------ Grade Management ------------------------
    def add_grade(self):
        print("\n--- Add New Grade ---")
        name = self.input_grade_selection("Select Grade Name to initialize configuration: ")
        if self.find_grade_by_name(name):
            print("Grade configurations already initialized.")
            return
        desc = input("Description (optional): ").strip()
        self.grades.append(Grade(name, desc))
        print("Grade configured successfully!")

    def view_all_grades(self):
        print("\n--- All Grades ---")
        if not self.grades:
            print("No configured grades found.")
            return
        for g in self.grades:
            print(f"Name: {g.name}, Description: {g.description}")

    def update_grade(self):
        print("\n--- Update Grade ---")
        name = self.input_grade_selection("Select configured Grade Name to update: ")
        grade = self.find_grade_by_name(name)
        if not grade:
            print("Grade configurations not initialized.")
            return
        new_desc = input(f"New Description (current: {grade.description}): ").strip()
        if new_desc:
            grade.description = new_desc
        print("Grade updated successfully!")

    def delete_grade(self):
        print("\n--- Delete Grade ---")
        name = self.input_grade_selection("Select configured Grade Name to delete: ")
        grade = self.find_grade_by_name(name)
        if not grade:
            print("Grade configurations not found.")
            return
        confirm = self.input_menu_choice(f"Delete configurations for '{name}'? (y/n): ", ['y', 'n', 'Y', 'N']).lower()
        if confirm == 'y':
            self.grades = [g for g in self.grades if g.name != name]
            for t in self.teachers:
                if name in t.assigned_grades:
                    t.assigned_grades.remove(name)
            for sub in self.subjects:
                if name in sub.assigned_grades:
                    sub.assigned_grades.remove(name)
            self.enrollments = [e for e in self.enrollments if e.grade_name != name]
            print("Grade information reset completed.")
        else:
            print("Deletion cancelled.")

    # ------------------------ Enrollment System ------------------------
    def enroll_student(self):
        print("\n--- Enroll Student into Grade ---")
        sid = self.input_int_only("Student ID: ")
        student = self.find_student_by_id(sid)
        if not student:
            print("Student not found.")
            return
        grade_name = self.input_grade_selection("Select target Grade option to enroll: ")
        for e in self.enrollments:
            if e.student_id == sid and e.grade_name == grade_name:
                print("Student already enrolled in this grade.")
                return
        self.enrollments.append(Enrollment(sid, grade_name))
        print(f"Student {student.name} enrolled in {grade_name}.")

    def view_enrollment_history(self):
        print("\n--- Enrollment History of a Student ---")
        sid = self.input_int_only("Student ID: ")
        student = self.find_student_by_id(sid)
        if not student:
            print("Student not found.")
            return
        history = [e for e in self.enrollments if e.student_id == sid]
        if not history:
            print(f"No enrollment records for {student.name}.")
            return
        print(f"Enrollment history for {student.name} (ID: {sid}):")
        for e in history:
            print(f"  Grade: {e.grade_name}, Date: {e.enroll_date}")

    # ------------------------ Score Management ------------------------
    def add_score(self):
        print("\n--- Add Score ---")
        sid = self.input_int_only("Student ID: ")
        if not self.find_student_by_id(sid):
            print("Student not found.")
            return
        sub_id = self.input_int_only("Subject ID: ")
        subject = self.find_subject_by_id(sub_id)
        if not subject:
            print("Subject not found.")
            return
        tid = input("Teacher ID (optional, press Enter to skip): ").strip()
        if tid:
            if not tid.isdigit() or not self.find_teacher_by_id(tid):
                print("Teacher not found. Score will be recorded without a linked teacher.")
                tid = ""
        while True:
            try:
                score_val = float(input("Score (0-100): ").strip())
                if 0 <= score_val <= 100:
                    break
                print("Score must be between 0 and 100.")
            except ValueError:
                print("Invalid score format. Please enter a valid numerical value.")
        self.scores.append(Score(sid, sub_id, tid, score_val))
        print("Score added successfully!")

    def view_all_scores(self):
        print("\n--- All Scores ---")
        if not self.scores:
            print("No scores recorded.")
            return
        for sc in self.scores:
            student = self.find_student_by_id(sc.student_id)
            subject = self.find_subject_by_id(sc.subject_id)
            teacher = self.find_teacher_by_id(sc.teacher_id) if sc.teacher_id else None
            stu_name = student.name if student else sc.student_id
            sub_name = subject.name if subject else sc.subject_id
            tea_name = teacher.name if teacher else "N/A"
            print(f"Student: {stu_name}, Subject: {sub_name}, Score: {sc.score}, Teacher: {tea_name}, Date: {sc.date}")

    def view_scores_for_student(self):
        print("\n--- Scores for a Student ---")
        sid = self.input_int_only("Student ID: ")
        student = self.find_student_by_id(sid)
        if not student:
            print("Student not found.")
            return
        student_scores = [sc for sc in self.scores if sc.student_id == sid]
        if not student_scores:
            print(f"No scores for {student.name}.")
            return
        print(f"Scores for {student.name} (ID: {sid}):")
        for sc in student_scores:
            subject = self.find_subject_by_id(sc.subject_id)
            sub_name = subject.name if subject else sc.subject_id
            print(f"  Subject: {sub_name}, Score: {sc.score}, Date: {sc.date}")

    def view_scores_for_teacher(self):
        print("\n--- Scores for a Teacher ---")
        tid = self.input_int_only("Teacher ID: ")
        teacher = self.find_teacher_by_id(tid)
        if not teacher:
            print("Teacher not found.")
            return
        teacher_scores = [sc for sc in self.scores if sc.teacher_id == tid]
        if not teacher_scores:
            print(f"No scores recorded for teacher {teacher.name}.")
            return
        print(f"Scores given by {teacher.name} (ID: {tid}):")
        for sc in teacher_scores:
            student = self.find_student_by_id(sc.student_id)
            subject = self.find_subject_by_id(sc.subject_id)
            stu_name = student.name if student else sc.student_id
            sub_name = subject.name if subject else sc.subject_id
            print(f"  Student: {stu_name}, Subject: {sub_name}, Score: {sc.score}, Date: {sc.date}")

    # ------------------------ Reports and Summaries ------------------------
    def list_students_by_grade(self):
        print("\n--- Students by Grade ---")
        grade_name = self.input_grade_selection("Select Grade to list associated enrollments: ")
        enrolled_students = [e.student_id for e in self.enrollments if e.grade_name == grade_name]
        if not enrolled_students:
            print(f"No students enrolled in {grade_name}.")
            return
        print(f"Students enrolled in {grade_name}:")
        for sid in enrolled_students:
            student = self.find_student_by_id(sid)
            if student:
                print(f"  ID: {sid}, Name: {student.name}")

    def generate_report_card(self):
        print("\n--- Student Report Card ---")
        sid = self.input_int_only("Student ID: ")
        student = self.find_student_by_id(sid)
        if not student:
            print("Student not found.")
            return
        student_scores = [sc for sc in self.scores if sc.student_id == sid]
        print(f"\n===== Report Card for {student.name} (ID: {sid}) =====")
        print(f"Grade: {student.grade}")
        print("Subjects and Scores:")
        if not student_scores:
            print("  No scores available.")
        else:
            for sc in student_scores:
                subject = self.find_subject_by_id(sc.subject_id)
                sub_name = subject.name if subject else sc.subject_id
                print(f"  {sub_name}: {sc.score}")
        print("=====================================")

    def view_total_counts(self):
        print("\n--- Total Counts ---")
        print(f"Total Students: {len(self.students)}")
        print(f"Total Teachers: {len(self.teachers)}")
        print(f"Total Subjects: {len(self.subjects)}")
        print(f"Total Grades: {len(self.grades)}")

    # ------------------------ Main Menu System ------------------------
    def display_main_menu(self):
        valid = [str(i) for i in range(1, 9)]
        while True:
            print("\n" + "=" * 50)
            print("      SCHOOL MANAGEMENT SYSTEM - MAIN MENU")
            print("=" * 50)
            print("1. Student Management")
            print("2. Teacher Management")
            print("3. Subject Management")
            print("4. Grade Management")
            print("5. Enrollment System")
            print("6. Score Management")
            print("7. Reports and Summaries")
            print("8. Save and Exit")
            choice = self.input_menu_choice("Enter your choice (1-8): ", valid)
            if choice == '1':
                self.student_menu()
            elif choice == '2':
                self.teacher_menu()
            elif choice == '3':
                self.subject_menu()
            elif choice == '4':
                self.grade_menu()
            elif choice == '5':
                self.enrollment_menu()
            elif choice == '6':
                self.score_menu()
            elif choice == '7':
                self.report_menu()
            elif choice == '8':
                self.save_all_data()
                print("Data saved. Goodbye!")
                break

    def student_menu(self):
        valid = [str(i) for i in range(1, 7)]
        while True:
            print("\n--- Student Management ---")
            print("1. Add Student")
            print("2. View All Students")
            print("3. Update Student")
            print("4. Delete Student")
            print("5. Search Student by ID")
            print("6. Back to Main Menu")
            sub = self.input_menu_choice("Choice: ", valid)
            if sub == '1':
                self.add_student()
            elif sub == '2':
                self.view_all_students()
            elif sub == '3':
                self.update_student()
            elif sub == '4':
                self.delete_student()
            elif sub == '5':
                self.search_student()
            elif sub == '6':
                break

    def teacher_menu(self):
        valid = [str(i) for i in range(1, 7)]
        while True:
            print("\n--- Teacher Management ---")
            print("1. Add Teacher")
            print("2. View All Teachers")
            print("3. Assign Teacher to Grade")
            print("4. Update Teacher")
            print("5. Delete Teacher")
            print("6. Back to Main Menu")
            sub = self.input_menu_choice("Choice: ", valid)
            if sub == '1':
                self.add_teacher()
            elif sub == '2':
                self.view_all_teachers()
            elif sub == '3':
                self.assign_teacher_to_grade()
            elif sub == '4':
                self.update_teacher()
            elif sub == '5':
                self.delete_teacher()
            elif sub == '6':
                break

    def subject_menu(self):
        valid = [str(i) for i in range(1, 5)]
        while True:
            print("\n--- Subject Management ---")
            print("1. Add Subject")
            print("2. View All Subjects")
            print("3. Assign Subject to Grade")
            print("4. Back to Main Menu")
            sub = self.input_menu_choice("Choice: ", valid)
            if sub == '1':
                self.add_subject()
            elif sub == '2':
                self.view_all_subjects()
            elif sub == '3':
                self.assign_subject_to_grade()
            elif sub == '4':
                break

    def grade_menu(self):
        valid = [str(i) for i in range(1, 6)]
        while True:
            print("\n--- Grade Management ---")
            print("1. Add Grade")
            print("2. View All Grades")
            print("3. Update Grade")
            print("4. Delete Grade")
            print("5. Back to Main Menu")
            sub = self.input_menu_choice("Choice: ", valid)
            if sub == '1':
                self.add_grade()
            elif sub == '2':
                self.view_all_grades()
            elif sub == '3':
                self.update_grade()
            elif sub == '4':
                self.delete_grade()
            elif sub == '5':
                break

    def enrollment_menu(self):
        valid = [str(i) for i in range(1, 4)]
        while True:
            print("\n--- Enrollment System ---")
            print("1. Enroll Student into Grade")
            print("2. View Enrollment History of a Student")
            print("3. Back to Main Menu")
            sub = self.input_menu_choice("Choice: ", valid)
            if sub == '1':
                self.enroll_student()
            elif sub == '2':
                self.view_enrollment_history()
            elif sub == '3':
                break

    def score_menu(self):
        valid = [str(i) for i in range(1, 6)]
        while True:
            print("\n--- Score Management ---")
            print("1. Add Score")
            print("2. View All Scores")
            print("3. View Scores for a Student")
            print("4. View Scores for a Teacher")
            print("5. Back to Main Menu")
            sub = self.input_menu_choice("Choice: ", valid)
            if sub == '1':
                self.add_score()
            elif sub == '2':
                self.view_all_scores()
            elif sub == '3':
                self.view_scores_for_student()
            elif sub == '4':
                self.view_scores_for_teacher()
            elif sub == '5':
                break

    def report_menu(self):
        valid = [str(i) for i in range(1, 5)]
        while True:
            print("\n--- Reports and Summaries ---")
            print("1. List Students by Grade")
            print("2. Generate Student Report Card")
            print("3. View Total Students, Teachers, Subjects")
            print("4. Back to Main Menu")
            sub = self.input_menu_choice("Choice: ", valid)
            if sub == '1':
                self.list_students_by_grade()
            elif sub == '2':
                self.generate_report_card()
            elif sub == '3':
                self.view_total_counts()
            elif sub == '4':
                break

# ---------------------------- Run Application ----------------------------
if __name__ == "__main__":
    system = SchoolSystem()
    system.display_main_menu()