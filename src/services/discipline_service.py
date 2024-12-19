from src.repository.repository_loader import RepositoryLoader
from src.repository.memory_repository import DisciplineMemoryRepository, GradeMemoryRepository
from src.repository.binary_repository import DisciplineBinaryRepository, GradeBinaryRepository
from src.repository.text_file_repository import DisciplineTextFileRepository, GradeTextFileRepository
from src.domain.dicipline import Discipline
from src.domain.dicipline import DisciplineValidator
from src.services.undo_service import FunctionCall, Operation, CascadedOperation

class DisciplineService:
    def __init__(self, undo_service, repository_loader: RepositoryLoader):
        repository_type = repository_loader.get_repository_type()
        if repository_type == "inmemory":
            self.__repository = DisciplineMemoryRepository()
            self.__grade_repository = GradeMemoryRepository()
        elif repository_type == "textfiles":
            self.__repository = DisciplineTextFileRepository(repository_loader.get_disciplines_file())
            self.__grade_repository = GradeTextFileRepository(repository_loader.get_grades_file())
        else:
            self.__repository = DisciplineBinaryRepository(repository_loader.get_disciplines_file())
            self.__grade_repository = GradeBinaryRepository(repository_loader.get_grades_file())

        self.undo_service = undo_service
        self.__discipline_validator = DisciplineValidator()

    def add_discipline(self, discipline_id, discipline_name):
        discipline = Discipline(discipline_id, discipline_name)
        self.__discipline_validator.validate(discipline)
        self.__repository.add_discipline(discipline)

        function_redo = FunctionCall(self.__repository.add_discipline, discipline)
        function_undo = FunctionCall(self.__repository.remove_discipline, discipline_id)
        self.undo_service.recordUndo(Operation(function_undo, function_redo))

    def remove_discipline(self, discipline_id):
        discipline = self.__repository.get_discipline_by_id(discipline_id)
        removed_grades = self.__grade_repository.remove_grade_by_discipline(discipline)
        self.__repository.remove_discipline(discipline_id)

        function_redo = FunctionCall(self.__repository.remove_discipline, discipline_id)
        function_undo = FunctionCall(self.__repository.add_discipline, discipline)
        operations = [Operation(function_undo, function_redo)]
        for grade in removed_grades:
            function_redo = FunctionCall(self.__grade_repository.remove_grade, grade)
            function_undo = FunctionCall(self.__grade_repository.add_grade, grade.student_id, grade.discipline_id, grade.grade_value)
            operations.append(Operation(function_undo, function_redo))
        self.undo_service.recordUndo(CascadedOperation(*operations))

    def update_discipline(self, discipline_id, new_discipline_name):
        old_discipline = self.__repository.get_discipline_by_id(discipline_id)
        old_discipline_name = old_discipline.discipline_name
        updated_discipline = self.__repository.update_discipline(discipline_id, new_discipline_name)
        function_redo = FunctionCall(self.__repository.update_discipline, discipline_id, new_discipline_name)
        function_undo = FunctionCall(self.__repository.update_discipline, discipline_id, old_discipline_name)
        self.undo_service.recordUndo(Operation(function_undo, function_redo))

        return updated_discipline

    def get_all_disciplines(self):
        return self.__repository.get_all_disciplines()

    def get_discipline_by_id(self, discipline_id):
        return self.__repository._data.get(discipline_id)

    def search_discipline(self, disciplines_list):
        return self.__repository.search_discipline(disciplines_list)