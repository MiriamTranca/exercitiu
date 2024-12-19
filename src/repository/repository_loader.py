from jproperties import Properties

from src.repository.binary_repository import StudentBinaryRepository, DisciplineBinaryRepository, GradeBinaryRepository
from src.repository.memory_repository import StudentMemoryRepository, DisciplineMemoryRepository, GradeMemoryRepository
from src.repository.text_file_repository import StudentTextFileRepository, DisciplineTextFileRepository, \
    GradeTextFileRepository


class RepositoryLoader:
    def __init__(self, file_name="settings.properties"):
        self.__file_name = file_name
        self.__repository_type = ""
        self.__students_file = ""
        self.__disciplines_file = ""
        self.__grades_file = ""

        self.__load_properties()

    def __load_properties(self):
        repository_manager = Properties()
        with open(self.__file_name, "rb") as settings_file:
            repository_manager.load(settings_file)

        self.__repository_type = repository_manager.get("repository").data
        self.__students_file = repository_manager.get("students").data
        self.__disciplines_file = repository_manager.get("disciplines").data
        self.__grades_file = repository_manager.get("grades").data

    def get_repository_type(self):
        return self.__repository_type

    def get_students_file(self):
        return self.__students_file

    def get_disciplines_file(self):
        return self.__disciplines_file

    def get_grades_file(self):
        return self.__grades_file

    def get_repository(self):
        repository_type = self.get_repository_type()

        if repository_type == "inmemory":
            return (StudentMemoryRepository(), DisciplineMemoryRepository(), GradeMemoryRepository())
        elif repository_type == "textfiles":
            return (StudentTextFileRepository(self.get_students_file()),
                    DisciplineTextFileRepository(self.get_disciplines_file()),
                    GradeTextFileRepository(self.get_grades_file()))
        elif repository_type == "binaryfiles":
            return (StudentBinaryRepository(self.get_students_file()),
                    DisciplineBinaryRepository(self.get_disciplines_file()),
                    GradeBinaryRepository(self.get_grades_file()))
        else:
            raise ValueError("Unsupported repository type")


