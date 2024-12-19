from src.domain.dicipline import Discipline
from src.domain.grade import Grade
from src.domain.student import Student
from src.repository.repository_loader import RepositoryLoader
from src.services.discipline_service import DisciplineService
from src.services.grade_service import GradeService
from src.services.student_service import StudentService
from faker import Faker
import random

from src.services.undo_service import UndoService

fake = Faker()

ADD_STUDENT = "1"
REMOVE_STUDENT = "2"
UPDATE_STUDENT = "3"
SHOW_ALL_STUDENTS = "4"

ADD_DISCIPLINE = "5"
REMOVE_DISCIPLINE = "6"
UPDATE_DISCIPLINE = "7"
SHOW_ALL_DISCIPLINES = "8"

GRADE_STUDENT_AT_GIVEN_DISCIPLINE = "9"
SHOW_ALL_GRADES = "10"

SEARCH_STUDENT = "11"
SEARCH_DISCIPLINE = "12"

UNDO_LAST_OPERATION = "13"
REDO_OPERATION = "14"

SHOW_FAILING_STUDENTS = "15"
SHOW_TOP_STUDENTS = "16"
SHOW_ALL_DISCIPLINES_WITH_GRADES = "17"

EXIT_PROGRAM = "0"

NUMBER_OF_ENTITIES_AVAILABLE_AT_START = 20

class UI:
    def __init__(self):
        repositories_loader = RepositoryLoader()
        self._undo_service = UndoService()

        self._student_service = StudentService(self._undo_service, repositories_loader)
        self._discipline_service = DisciplineService(self._undo_service, repositories_loader)
        self._grade_service = GradeService(self._undo_service, repositories_loader, self._discipline_service, self._student_service)
        self.populate_data()

    def populate_data(self):
        students = self.generate_students()
        disciplines = self.generate_disciplines()
        grades = self.generate_grades(students, disciplines)

        for student in students:
            self._student_service.add_student(student.student_id, student.student_name)
        for discipline in disciplines:
            self._discipline_service.add_discipline(discipline.discipline_id, discipline.discipline_name)
        for grade in grades:
            self._grade_service.add_grade(grade.student_id, grade.discipline_id, grade.grade_value)

    def print_menu(self):
        print(ADD_STUDENT +". Add new student.")
        print(REMOVE_STUDENT +". Remove student.")
        print(UPDATE_STUDENT +". Update student.")
        print(SHOW_ALL_STUDENTS+". Show all students.")
        print(ADD_DISCIPLINE +". Add new discipline.")
        print(REMOVE_DISCIPLINE +". Remove discipline.")
        print(UPDATE_DISCIPLINE +". Update discipline.")
        print(SHOW_ALL_DISCIPLINES+". Show all disciplines.")
        print(GRADE_STUDENT_AT_GIVEN_DISCIPLINE +". Add grade for student.")
        print(SHOW_ALL_GRADES+". Show all grades.")
        print(SEARCH_STUDENT + ". Search students.")
        print(SEARCH_DISCIPLINE + ". Search disciplines.")
        print(UNDO_LAST_OPERATION + ". Undo last operation.")
        print(REDO_OPERATION + ". Redo operation.")
        print(SHOW_FAILING_STUDENTS + ". Show failing students.")
        print(SHOW_TOP_STUDENTS + ". Show top students.")
        print(SHOW_ALL_DISCIPLINES_WITH_GRADES + ". Show all disciplines with grades.")
        print(EXIT_PROGRAM +". Exit program.")

    def start(self):
        while True:
            self.print_menu()
            try:
                user_choice = input("Enter your choice: ")
                if user_choice == EXIT_PROGRAM:
                    break
                elif user_choice == ADD_STUDENT:
                    self.__add_student_ui()
                elif user_choice == REMOVE_STUDENT:
                    self.__remove_student_ui()
                elif user_choice == UPDATE_STUDENT:
                    self.__update_student_ui()
                elif user_choice == SHOW_ALL_STUDENTS:
                    self.__show_all_students_ui()
                elif user_choice == ADD_DISCIPLINE:
                    self.__add_discipline_ui()
                elif user_choice == REMOVE_DISCIPLINE:
                    self.__remove_discipline_ui()
                elif user_choice == UPDATE_DISCIPLINE:
                    self.__update_discipline_ui()
                elif user_choice == SHOW_ALL_DISCIPLINES:
                    self.__show_all_disciplines_ui()
                elif user_choice == GRADE_STUDENT_AT_GIVEN_DISCIPLINE:
                    self.__grade_student_ui()
                elif user_choice == SHOW_ALL_GRADES:
                    self.__show_all_grades_ui()
                elif user_choice == SEARCH_STUDENT:
                    self.__search_student_ui()
                elif user_choice == SEARCH_DISCIPLINE:
                    self.__search_discipline_ui()
                elif user_choice == UNDO_LAST_OPERATION:
                    self.__undo_ui()
                elif user_choice == REDO_OPERATION:
                    self.__redo_ui()
                elif user_choice == SHOW_FAILING_STUDENTS:
                    self.__show_failing_students_ui()
                elif user_choice == SHOW_TOP_STUDENTS:
                    self.__show_top_5_students_ui()
                elif user_choice == SHOW_ALL_DISCIPLINES_WITH_GRADES:
                    self.__show_all_disciplines_with_grades_ui()
            except Exception as error:
                print(error)

    def __add_student_ui(self):
        student_id = input("Enter student ID: ")
        student_name = input("Enter student name: ")
        self._student_service.add_student(student_id, student_name)

    def __add_discipline_ui(self):
        discipline_id = input("Enter discipline ID: ")
        discipline_name = input("Enter discipline name: ")
        self._discipline_service.add_discipline(discipline_id, discipline_name)

    def __remove_student_ui(self):
        student_id = input("Enter student ID: ")
        self._grade_service.remove_grades_for_student(student_id)
        self._student_service.remove_student(student_id)

    def __remove_discipline_ui(self):
        discipline_id = input("Enter discipline ID: ")
        self._grade_service.remove_grades_for_discipline(discipline_id)
        self._discipline_service.remove_discipline(discipline_id)

    def __update_student_ui(self):
        student_id = input("Enter student ID: ")
        student_name = input("Enter new student name: ")
        self._student_service.update_student(student_id, student_name)

    def __update_discipline_ui(self):
        discipline_id = input("Enter discipline ID: ")
        discipline_name = input("Enter new discipline name: ")
        self._discipline_service.update_discipline(discipline_id, discipline_name)

    def __show_all_students_ui(self):
        students = self._student_service.get_all_students()
        for student in students:
            print(student)

    def __show_all_disciplines_ui(self):
        disciplines = self._discipline_service.get_all_disciplines()
        for discipline in disciplines:
            print(discipline)

    def __grade_student_ui(self):
        student_id = input("Enter student ID: ")
        discipline_id = input("Enter discipline ID: ")
        grade_value = input("Enter grade value: ")

        self._grade_service.add_grade(student_id, discipline_id, grade_value)

    def __show_all_grades_ui(self):
        grades = self._grade_service.get_all_grades()
        for grade in grades:
            print(grade)

    def __search_student_ui(self):
        search_query = input("Enter search string for students: ")
        students = self._student_service.search_students(search_query)

        if students:
            print("Matching students found:")
            for student in students:
                print(f"Student ID: {student.student_id}, Student Name: {student.student_name}")
        else:
            print("No students found matching the search term.")

    def __search_discipline_ui(self):
        search_query = input("Enter search string for disciplines: ")
        disciplines = self._discipline_service.search_discipline(search_query)

        if disciplines:
            print("Matching disciplines found:")
            for discipline in disciplines:
                print(f"Discipline ID: {discipline.discipline_id}, Discipline Name: {discipline.discipline_name}")
        else:
            print("No disciplines found matching the search term.")

    def __undo_ui(self):
        self._undo_service.undo()

    def __redo_ui(self):
        self._undo_service.redo()

    def __show_failing_students_ui(self):
        failing_students = self._grade_service.statistic_all_students_failing()
        if failing_students:
            print("Students failing at least one discipline:")
            for student_discipline in failing_students:
                student = student_discipline.student
                print(f"Student ID: {student.student_id}, Student Name: {student.student_name}")
        else:
            print("No students are failing at least one discipline.")

    def __show_top_5_students_ui(self):
        top_students = self._grade_service.statistic_first_5_students_with_best_school_situation()
        if top_students:
            print("Top 5 students with the best school situation (highest aggregated average):")
            for index, (student, average) in enumerate(top_students, 1):
                print(f"{index}. Student ID: {student.student_id}, Student Name: {student.student_name}")
        else:
            print("No students found.")

    def __show_all_disciplines_with_grades_ui(self):
        disciplines = self._grade_service.statistic_all_disciplines_with_grades()
        if disciplines:
            print("Disciplines with average grades (sorted by average grade in descending order):")
            for index, (discipline, average_grade) in enumerate(disciplines, 1):
                print(f"{index}. Discipline: {discipline.discipline_name}, Average Grade: {average_grade:.2f}")
        else:
            print("No grades available for any discipline.")

    def generate_students(self):
        students = []
        for _ in range(NUMBER_OF_ENTITIES_AVAILABLE_AT_START):
            student_id = fake.uuid4().replace("-", "")[:10]
            student_name = ''.join(filter(str.isalpha, fake.name()))
            students.append(Student(student_id, student_name))
        return students

    def generate_disciplines(self):
        disciplines = []
        discipline_names = ["Romanian", "English", "German", "Math", "CS", "Biology", "Chemistry", "Physics", "History", "Geography", "Literature", "Economics", "Psychology",
    "Philosophy", "Sociology", "Art", "Music", "Law", "Engineering", "Architecture",
    "Medicine"]
        for _ in range(NUMBER_OF_ENTITIES_AVAILABLE_AT_START):
            discipline_id = fake.uuid4().replace("-", "")[:10]
            discipline_name = random.choice(discipline_names)
            disciplines.append(Discipline(discipline_id, discipline_name))
        return disciplines

    def generate_grades(self, students, disciplines):
        grades = []
        for _ in range(NUMBER_OF_ENTITIES_AVAILABLE_AT_START):
            student = random.choice(students)
            discipline = random.choice(disciplines)
            grade_value = random.randint(1, 10)
            grade_value = str(grade_value)
            grades.append(
                Grade(discipline.discipline_id, student.student_id, grade_value))

        return grades

if __name__ == "__main__":
    ui = UI()
    ui.start()