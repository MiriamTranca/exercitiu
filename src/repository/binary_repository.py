import pickle
from src.repository.memory_repository import DuplicateIDError, IDNotFoundError, StudentMemoryRepository, \
    DisciplineMemoryRepository, GradeMemoryRepository


class StudentBinaryRepository(StudentMemoryRepository):
    def __init__(self, file_name):
        self.file_name = file_name
        self._data = self._load_data()

    def _load_data(self):
        with open(self.file_name, "rb") as file:
            return pickle.load(file)

    def _save_data(self):
        with open(self.file_name, "wb") as file:
            pickle.dump(self._data, file)

    def add_student(self, student):
        if student.student_id in self._data:
            raise DuplicateIDError("Duplicate student ID")
        self._data[student.student_id] = student
        self._save_data()

    def remove_student(self, student_id):
        if student_id not in self._data:
            raise IDNotFoundError("ID not found")
        del self._data[student_id]
        self._save_data()

    def update_student(self, student_id, new_student_name):
        if student_id not in self._data:
            raise IDNotFoundError("ID not found")
        student = self._data[student_id]
        student.student_name = new_student_name
        self._save_data()

    def get_all_students(self):
        return list(self._data.values())

    def search_student(self, search_term: str):
        search_term = search_term.lower()
        return [
            student for student in self._data.values()
            if search_term in student.student_name.lower() or search_term in student.student_id.lower()
        ]

class DisciplineBinaryRepository(DisciplineMemoryRepository):
    def __init__(self, file_name):
        self.file_name = file_name
        self._data = self._load_data()

    def _load_data(self):
         with open(self.file_name, "rb") as file:
                return pickle.load(file)

    def _save_data(self):
        with open(self.file_name, "wb") as file:
            pickle.dump(self._data, file)

    def add_discipline(self, discipline):
        if discipline.discipline_id in self._data:
            raise DuplicateIDError("Duplicate discipline ID")
        self._data[discipline.discipline_id] = discipline
        self._save_data()

    def remove_discipline(self, discipline_id):
        if discipline_id not in self._data:
            raise IDNotFoundError("ID not found")
        del self._data[discipline_id]
        self._save_data()

    def update_discipline(self, discipline_id, new_discipline_name):
        if discipline_id not in self._data:
            raise IDNotFoundError("ID not found")
        discipline = self._data[discipline_id]
        discipline.discipline_name = new_discipline_name
        self._save_data()

    def get_all_disciplines(self):
        return list(self._data.values())

    def search_discipline(self, search_term: str):
        search_term = search_term.lower()

        return [
            discipline for discipline in self._data.values()
            if search_term in discipline.discipline_name.lower() or search_term in discipline.discipline_id.lower()
        ]


class GradeBinaryRepository(GradeMemoryRepository):
    def __init__(self, file_name):
        self.file_name = file_name
        self._data = self._load_data()

    def _load_data(self):
        with open(self.file_name, "rb") as file:
            return pickle.load(file)

    def _save_data(self):
        with open(self.file_name, "wb") as file:
            pickle.dump(self._data, file)

    def add_grade(self, grade):
        if grade.student_id not in self._data:
            self._data[grade.student_id] = {}

        if grade.discipline_id not in self._data[grade.student_id]:
            self._data[grade.student_id][grade.discipline_id] = []

        self._data[grade.student_id][grade.discipline_id].append(grade)
        self._save_data()

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

    def remove_grade_by_student(self, student_id):
        if student_id in self._data:
            removed_grades = []
            for discipline_id, grades in self._data[student_id].items():
                removed_grades.extend(grades)
            del self._data[student_id]
            self._save_data()
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
        self._save_data()
        return removed_grades
