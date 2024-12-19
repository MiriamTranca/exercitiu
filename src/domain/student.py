class Student:
    def __init__(self, student_id, student_name):
        self.__student_id = student_id
        self.__student_name = student_name

    @property
    def student_id(self):
        return self.__student_id

    @property
    def student_name(self):
        return self.__student_name

    @student_id.setter
    def student_id(self, new_student_id):
        self.__student_id = new_student_id

    @student_name.setter
    def student_name(self, new_student_name):
        self.__student_name = new_student_name

    def __str__(self):
        return "Student ID: " + self.__student_id + ", Name: " + self.__student_name

class StudentValidator:
    def validate(self, student):
        if isinstance(student, Student) is False:
            raise TypeError("Not a  Student")

        if not student.student_name.isalpha():
            raise ValidatorException("Student name should contain only letters")

class ValidatorException(Exception):
    def __init__(self, message = "Validation error"):
        self._message = message

    @property
    def message(self):
        return self._message

