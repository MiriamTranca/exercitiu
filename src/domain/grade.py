class Grade:
    def __init__(self, discipline_id, student_id, grade_value):
        self.__discipline_id = discipline_id
        self.__student_id = student_id
        self.__grade_value = grade_value

    @property
    def discipline_id(self):
        return self.__discipline_id

    @property
    def student_id(self):
        return self.__student_id

    @property
    def grade_value(self):
        return self.__grade_value


    @discipline_id.setter
    def discipline_id(self, new_discipline_id):
        self.__discipline_id = new_discipline_id

    @student_id.setter
    def student_id(self, new_student_id):
        self.__student_id = new_student_id

    @grade_value.setter
    def grade_value(self, new_grade_value):
        self.__grade_value = new_grade_value

    def __str__(self):
        return "Student ID: " + self.__student_id + ", Discipline ID: " + self.__discipline_id + ", Grade Value: " + self.__grade_value

class GradeValidator:
    def validate(self, grade):
        if isinstance(grade, Grade) is False:
            raise TypeError("Not a Grade")
        if int(grade.grade_value) < 0 or int(grade.grade_value) > 10:
            raise ValidatorException()

class ValidatorException(Exception):
    def __init__(self, message="Validation error"):
        self._message = message

    @property
    def message(self):
        return self._message

