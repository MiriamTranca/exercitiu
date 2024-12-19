from src.domain import grade
from src.repository.repository_loader import RepositoryLoader
from src.repository.memory_repository import GradeMemoryRepository, IDNotFoundError
from src.repository.binary_repository import GradeBinaryRepository
from src.repository.text_file_repository import GradeTextFileRepository

from src.domain.grade import GradeValidator, Grade
from src.services.discipline_service import DisciplineService
from src.services.student_service import StudentService
from src.services.undo_service import FunctionCall, Operation

NUMBER_OF_FIRST_STUDENTS = 5
MINIMUM_GRADE_TO_PASS = 5
STARTING_INDEX = 1

class StudentDisciplineDTO:
    def __init__(self, student, discipline):
        self._student = student
        self._discipline = discipline

    @property
    def student(self):
        return self._student

    @property
    def discipline(self):
        return self._discipline

class GradeService:
    def __init__(self, undo_service, repository_loader: RepositoryLoader, discipline_service: DisciplineService, student_service:StudentService):

        self.__discipline_service = discipline_service
        self.__student_service = student_service
        self.__validator = GradeValidator()
        repository_type = repository_loader.get_repository_type()
        if repository_type == "inmemory":
            self.__repository = GradeMemoryRepository()
        elif repository_type == "textfiles":
            self.__repository = GradeTextFileRepository(repository_loader.get_grades_file())
        else:
            self.__repository = GradeBinaryRepository(repository_loader.get_grades_file())

        self.undo_service = undo_service

    def add_grade(self, student_id, discipline_id, grade_value):
        student = self.__student_service.get_student_by_id(student_id)
        if not student:
            raise IDNotFoundError(f"Student with ID {student_id} not found.")

        discipline = self.__discipline_service.get_discipline_by_id(discipline_id)
        if not discipline:
            raise IDNotFoundError(f"Discipline with ID {discipline_id} not found.")

        grade = Grade( discipline_id, student_id, grade_value)
        self.__validator.validate(grade)
        self.__repository.add_grade(grade)

        function_redo = FunctionCall(self.__repository.add_grade, grade)
        function_undo = FunctionCall(self.__repository.remove_grade, grade)
        self.undo_service.recordUndo(Operation(function_undo, function_redo))

    def get_all_grades(self):
        return self.__repository.get_all_grades()

    def get_grades_for_student(self, student_id):
        return self.__repository.get_grades_by_student(student_id)

    def remove_grade(self, grade):
        return self.__repository.remove_grade(grade)

    def remove_grades_for_student(self, student_id):
        return self.__repository.remove_grade_by_student(student_id)

    def remove_grades_for_discipline(self, discipline_id):
        return self.__repository.remove_grade_by_discipline(discipline_id)

    def statistic_all_students_failing(self):
        failing_students = []
        seen_students = []

        grades = self.get_all_grades()
        student_disciplines = {}

        for grade in grades:
            student_id = grade.student_id
            discipline_id = grade.discipline_id
            grade_value = int(grade.grade_value)

            if student_id not in student_disciplines:
                student_disciplines[student_id] = {}

            if discipline_id not in student_disciplines[student_id]:
                student_disciplines[student_id][discipline_id] = []

            student_disciplines[student_id][discipline_id].append(grade_value)

        for student_id, disciplines in student_disciplines.items():
            student = self.__student_service.get_student_by_id(student_id)
            if student:
                failing = False
                for discipline_id, grades in disciplines.items():
                    average_grade = sum(grades) / len(grades)
                    if average_grade < MINIMUM_GRADE_TO_PASS:
                        failing = True
                        discipline = self.__discipline_service.get_discipline_by_id(discipline_id)
                        if student.student_id not in seen_students:
                            failing_students.append(StudentDisciplineDTO(student, discipline))
                            seen_students.append(student.student_id)
                        break
                if failing:
                    seen_students.append(student.student_id)

        return failing_students

    def statistic_first_5_students_with_best_school_situation(self):
        student_grades = {}
        grades = self.get_all_grades()

        for grade in grades:
            student_id = grade.student_id
            discipline_id = grade.discipline_id
            grade_value = int(grade.grade_value)

            if student_id not in student_grades:
                student_grades[student_id] = {}

            if discipline_id not in student_grades[student_id]:
                student_grades[student_id][discipline_id] = []

            student_grades[student_id][discipline_id].append(grade_value)

        student_aggregated_averages = []

        for student_id, disciplines in student_grades.items():
            student = self.__student_service.get_student_by_id(student_id)
            if student:
                total_average = 0
                total_disciplines = 0
                for discipline_id, grades in disciplines.items():
                    average_grade = sum(grades) / len(grades)
                    total_average += average_grade
                    total_disciplines += 1
                overall_average = total_average / total_disciplines if total_disciplines > 0 else 0
                student_aggregated_averages.append((student, overall_average))

        student_aggregated_averages.sort(key=lambda x: x[STARTING_INDEX], reverse=True)
        first_students = student_aggregated_averages[:NUMBER_OF_FIRST_STUDENTS]

        first_students_dto = []
        for student, overall_average in first_students:
            first_students_dto.append((student, overall_average))

        return first_students_dto

    def statistic_all_disciplines_with_grades(self):
        discipline_grades = {}
        grades = self.get_all_grades()

        for grade in grades:
            discipline_id = grade.discipline_id
            grade_value = int(grade.grade_value)

            if discipline_id not in discipline_grades:
                discipline_grades[discipline_id] = {"total_grades": 0, "count": 0}

            discipline_grades[discipline_id]["total_grades"] += grade_value
            discipline_grades[discipline_id]["count"] += 1

        discipline_averages = []

        for discipline_id, data in discipline_grades.items():
            average_grade = data["total_grades"] / data["count"]
            discipline = self.__discipline_service.get_discipline_by_id(
                discipline_id)
            discipline_averages.append((discipline, average_grade))

        discipline_averages.sort(key=lambda x: x[STARTING_INDEX], reverse=True)

        return discipline_averages
