class Discipline:
    def __init__(self, discipline_id, discipline_name):
        self.__discipline_id = discipline_id
        self.__discipline_name = discipline_name

    @property
    def discipline_id(self):
        return self.__discipline_id

    @property
    def discipline_name(self):
        return self.__discipline_name

    @discipline_id.setter
    def discipline_id(self, new_discipline_id):
        self.__discipline_id = new_discipline_id

    @discipline_name.setter
    def discipline_name(self, new_discipline_name):
        self.__discipline_name = new_discipline_name

    def __str__(self):
        return "Discipline ID: " + self.__discipline_id + ", Discipline: " + self.__discipline_name

class DisciplineValidator:
    def validate(self, discipline):
        if isinstance(discipline, Discipline) is  False:
            raise TypeError("Not a Discipline")

        if not discipline.discipline_name.isalpha():
            raise ValidatorException("Discipline name should contain only letters")

class ValidatorException(Exception):
    def __init__(self, message="Validation error"):
        self._message = message

    @property
    def message(self):
        return self._message


