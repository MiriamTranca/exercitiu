from src.domain.dicipline import Discipline
from src.domain.grade import Grade
from src.domain.student import Student

from src.repository.memory_repository import StudentMemoryRepository, DuplicateIDError, IDNotFoundError, \
    DisciplineMemoryRepository



def test_discipline():
    new_discipline = Discipline(discipline_id="1", discipline_name="<NAME>")
    assert new_discipline.discipline_id == "1"
    assert new_discipline.discipline_name == "<NAME>"

def test_student():
    new_student = Student(student_id="1", student_name="<NAME>")
    assert new_student.student_id == "1"
    assert new_student.student_name == "<NAME>"

def test_grade():
    new_grade = Grade(discipline_id="1", student_id="1", grade_value="5")
    assert new_grade.discipline_id == "1"
    assert new_grade.student_id == "1"
    assert new_grade.grade_value == "5"

def test_add_student():
    repository = StudentMemoryRepository()

    try:
        student1 = Student("S12345", "Alice Johnson")
        repository.add_student(student1)
        student2 = Student("S12345", "Bob Smith",)
        repository.add_student(student2)

    except DuplicateIDError:
        assert True

def test_remove_student():
    repository = StudentMemoryRepository()

    student1 = Student("S12345", "Alice Johnson")
    repository.add_student(student1)
    student2 = Student("S67890", "Bob Smith")
    repository.add_student(student2)

    removed_student = repository.remove_student("S12345")
    assert removed_student.student_id == "S12345"
    assert len(repository.get_all_students()) == 1

    try:
        repository.remove_student("S00000")
    except IDNotFoundError:
        assert True

def test_update_student():
    repository = StudentMemoryRepository()

    student1 = Student("S12345", "Alice Johnson")
    repository.add_student(student1)

    updated_student = repository.update_student("S12345", "Alice Brown")
    assert updated_student.student_name == "Alice Brown"

    try:
        repository.update_student("S00000", "Unknown Student")
    except IDNotFoundError:
        assert True

def test_get_all_students():
    repository = StudentMemoryRepository()

    student1 = Student("S12345", "Alice Johnson")
    repository.add_student(student1)
    student2 = Student("S67890", "Bob Smith")
    repository.add_student(student2)

    students = repository.get_all_students()
    assert len(students) == 2

    student_ids = [student.student_id for student in students]
    assert "S12345" in student_ids
    assert "S67890" in student_ids

def test_add_discipline():
    repository = DisciplineMemoryRepository()

    discipline1 = Discipline("D12345", "Mathematics")
    repository.add_discipline(discipline1)
    assert len(repository.get_all_disciplines()) == 1

    try:
        discipline2 = Discipline("D12345", "Physics")
        repository.add_discipline(discipline2)
    except DuplicateIDError:
        assert True

def test_remove_discipline():
    repository = DisciplineMemoryRepository()

    discipline1 = Discipline("D12345", "Mathematics")
    repository.add_discipline(discipline1)
    discipline2 = Discipline("D67890", "Physics")
    repository.add_discipline(discipline2)

    removed_discipline = repository.remove_discipline("D12345")
    assert removed_discipline.discipline_id == "D12345"
    assert len(repository.get_all_disciplines()) == 1

    try:
        repository.remove_discipline("D00000")
    except IDNotFoundError:
        assert True

def test_update_discipline():
    repository = DisciplineMemoryRepository()

    discipline1 = Discipline("D12345", "Mathematics")
    repository.add_discipline(discipline1)

    updated_discipline = repository.update_discipline("D12345", "Advanced Mathematics")
    assert updated_discipline.discipline_name == "Advanced Mathematics"

    try:
        repository.update_discipline("D00000", "New Discipline")
    except IDNotFoundError:
        assert True

def test_get_all_disciplines():
    repository = DisciplineMemoryRepository()

    discipline1 = Discipline("D12345", "Mathematics")
    repository.add_discipline(discipline1)
    discipline2 = Discipline("D67890", "Physics")
    repository.add_discipline(discipline2)

    disciplines = repository.get_all_disciplines()
    assert len(disciplines) == 2

    discipline_ids = [discipline.discipline_id for discipline in disciplines]
    assert "D12345" in discipline_ids
    assert "D67890" in discipline_ids


if __name__ == '__main__':
    test_discipline()
    test_student()
    test_grade()
    test_add_student()
    test_remove_student()
    test_update_student()
    test_get_all_students()
    test_add_discipline()
    test_remove_discipline()
    test_update_discipline()
    test_get_all_disciplines()


