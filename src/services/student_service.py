from src.domain.student import StudentValidator, Student
from src.repository.binary_repository import StudentBinaryRepository, GradeBinaryRepository
from src.repository.memory_repository import StudentMemoryRepository, GradeMemoryRepository
from src.repository.repository_loader import RepositoryLoader
from src.repository.text_file_repository import StudentTextFileRepository, GradeTextFileRepository
from src.services.undo_service import FunctionCall, Operation, CascadedOperation, UndoService


class StudentService:
    def __init__(self, undo_service, repository_loader: RepositoryLoader):

        repository_type = repository_loader.get_repository_type()
        if repository_type == "inmemory":
            self.__repository = StudentMemoryRepository()
            self.__grade_repository = GradeMemoryRepository()
        elif repository_type == "textfiles":
            self.__repository = StudentTextFileRepository(repository_loader.get_students_file())
            self.__grade_repository = GradeTextFileRepository(repository_loader.get_grades_file())
        else:
            self.__repository = StudentBinaryRepository(repository_loader.get_students_file())
            self.__grade_repository = GradeBinaryRepository(repository_loader.get_grades_file())

        self.__validator = StudentValidator()
        self.undo_service = undo_service

    def add_student(self, student_id, student_name):
        student = Student(student_id, student_name)
        self.__validator.validate(student)
        self.__repository.add_student(student)

        function_redo = FunctionCall(self.__repository.add_student, student)
        function_undo = FunctionCall(self.__repository.remove_student, student_id)
        self.undo_service.recordUndo(Operation(function_undo, function_redo))

    def remove_student(self, student_id):
        student = self.__repository.get_student_by_id(student_id)
        removed_grades = self.__grade_repository.get_grades_by_student(student_id)

        self.__repository.remove_student(student_id)

        function_redo = FunctionCall(self.__repository.remove_student, student_id)
        function_undo = FunctionCall(self.__repository.add_student, student)
        operations = [Operation(function_undo, function_redo)]

        for grade in removed_grades:
            function_redo = FunctionCall(self.__grade_repository.remove_grade, grade)
            function_undo = FunctionCall(self.__grade_repository.add_grade, grade.student_id, grade.discipline_id, grade.grade_value)
            operations.append(Operation(function_undo, function_redo))
        self.undo_service.recordUndo(CascadedOperation(*operations))

    def update_student(self, student_id, new_student_name):
        old_student = self.__repository.get_student_by_id(student_id)
        old_student_name = old_student.student_name

        updated_student = self.__repository.update_student(student_id, new_student_name)

        function_redo = FunctionCall(self.__repository.update_student, student_id, new_student_name)
        function_undo = FunctionCall(self.__repository.update_student, student_id, old_student_name)
        self.undo_service.recordUndo(Operation(function_undo, function_redo))
        return updated_student

    def get_all_students(self):
        return self.__repository.get_all_students()

    def get_student_by_id(self, student_id):
        return self.__repository._data.get(student_id)

    def search_students(self, students_list):
        return self.__repository.search_student(students_list)