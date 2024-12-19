
class RepositoryError(Exception):
    pass

class DuplicateIDError(Exception):
    pass

class IDNotFoundError(Exception):
    pass

class RepositoryIterator:
    def __init__(self, data):
        self.__data = data
        self.__position = -1
    def __next__(self):
        self.__position += 1
        if len(self.__data) == self.__position:
            raise StopIteration()
        return self.__data[self.__position]

class StudentMemoryRepository:
    def __init__(self):
        self._data = {}

    def add_student(self, student):
        if student.student_id in self._data:
            raise DuplicateIDError("Duplicate student ID")
        self._data[student.student_id] = student

    def remove_student(self, student_id):
        if student_id not in self._data:
            raise IDNotFoundError("ID not found")
        return self._data.pop(student_id)

    def get_student_by_id(self, student_id):
        return self._data.get(student_id)

    def update_student(self, student_id, new_student_name):
        if student_id not in self._data:
            raise IDNotFoundError("ID not found")
        student = self._data[student_id]
        if new_student_name:
            student.student_name = new_student_name
        return student

    def get_all_students(self):
        return self._data.values()

    def search_student(self, search_term: str):
        search_term = search_term.lower()
        matching_students = [
            student for student in self._data.values() if
            search_term in student.student_name.lower() or search_term in str(student.student_id).lower()
        ]
        return matching_students

class DisciplineMemoryRepository:
    def __init__(self):
        self._data = {}

    def add_discipline(self, discipline):
        if discipline.discipline_id in self._data:
            raise DuplicateIDError("Duplicate discipline ID")
        self._data[discipline.discipline_id] = discipline

    def remove_discipline(self, discipline_id):
        if discipline_id not in self._data:
            raise IDNotFoundError("ID not found")
        return self._data.pop(discipline_id)

    def update_discipline(self, discipline_id, new_discipline_name):
        if discipline_id not in self._data:
            raise IDNotFoundError("ID not found")
        discipline = self._data[discipline_id]
        if new_discipline_name:
            discipline.discipline_name = new_discipline_name
        return discipline

    def get_discipline_by_id(self, discipline_id):
        return self._data.get(discipline_id)

    def get_all_disciplines(self):
        return self._data.values()

    def search_discipline(self, search_term: str):
        search_term = search_term.lower()
        matching_disciplines = [
            discipline for discipline in self._data.values() if
            search_term in discipline.discipline_name.lower() or search_term in str(discipline.discipline_id).lower()
        ]
        return matching_disciplines


class GradeMemoryRepository:
    def __init__(self):
        self._data = {}

    def add_grade(self, grade):
        if grade.student_id not in self._data:
            self._data[grade.student_id] = {}

        if grade.discipline_id not in self._data[grade.student_id]:
            self._data[grade.student_id][grade.discipline_id] = []

        self._data[grade.student_id][grade.discipline_id].append(grade)

    def get_all_grades(self):
        all_grades = []
        for student_grades in self._data.values():
            for grades in student_grades.values():
                all_grades.extend(grades)
        return all_grades

    def remove_grade(self, grade):
        student_grades = self._data.get(grade.student_id, {})
        if grade.discipline_id in student_grades:
            grades = student_grades[grade.discipline_id]
            if grade in grades:
                grades.remove(grade)
                if not grades:
                    del student_grades[grade.discipline_id]
                if not student_grades:
                    del self._data[grade.student_id]

    def get_grades_by_student(self, student_id):
        if student_id in self._data:
            grades_list = []
            for discipline_id, grades in self._data[student_id].items():
                grades_list.append(grades)
            return grades_list
        return []

    def remove_grade_by_student(self, student_id):
        if student_id in self._data:
            removed_grades = []
            for discipline_id, grades in self._data[student_id].items():
                removed_grades.extend(grades)
            del self._data[student_id]
            return removed_grades
        return []

    def remove_grade_by_discipline(self, discipline_id):
        removed_grades = []
        for student_id, student_grades in list(self._data.items()):
            if discipline_id in student_grades:
                removed_grades.extend(student_grades[discipline_id])
                del student_grades[discipline_id]
            if not student_grades:
                del self._data[student_id]
        return removed_grades



