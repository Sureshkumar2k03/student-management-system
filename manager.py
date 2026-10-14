"""OOP: StudentManager holds all students and exposes the operations."""

from collections import Counter

from decorators import log_call, timed
from exceptions import DuplicateStudentError, StudentNotFoundError
from generators import generate_students
from models import Student
from storage import DATA_FILE, load_students, save_students


class StudentManager:
    def __init__(self, path=DATA_FILE):
        self.path = path
        self._students = {}          # dict: student_id -> Student
        self.load()

    # --- persistence ---------------------------------------------------
    @timed
    def load(self):
        self._students = {s.student_id: s for s in load_students(self.path)}

    def save(self):
        save_students(self._students.values(), self.path)

    # --- CRUD ----------------------------------------------------------
    @log_call
    def add(self, student_id, name, age, course, marks=None):
        student_id = str(student_id).strip()
        if student_id in self._students:
            raise DuplicateStudentError(student_id)
        student = Student(student_id, name, age, course, marks)
        self._students[student_id] = student
        self.save()
        return student

    def get(self, student_id):
        try:
            return self._students[str(student_id).strip()]
        except KeyError:
            raise StudentNotFoundError(student_id) from None

    @log_call
    def update(self, student_id, name, age, course, marks=None):
        old = self.get(student_id)
        updated = Student(old.student_id, name, age, course,
                          old.marks if marks is None else marks)
        self._students[old.student_id] = updated
        self.save()
        return updated

    @log_call
    def delete(self, student_id):
        student = self.get(student_id)
        del self._students[student.student_id]
        self.save()
        return student

    # --- queries -------------------------------------------------------
    def all(self):
        return sorted(self._students.values(), key=lambda s: s.student_id)

    def search(self, text):
        text = text.lower().strip()
        return [s for s in self.all()
                if text in s.name.lower() or text in s.student_id.lower()
                or text in s.course.lower()]

    def ranked(self):
        return sorted(self._students.values(), key=lambda s: s.average, reverse=True)

    def stats(self):
        students = self.all()
        if not students:
            return {"count": 0, "class_average": 0, "topper": None,
                    "grades": {}, "courses": {}}
        grades = Counter(s.grade for s in students)
        courses = Counter(s.course for s in students)
        return {
            "count": len(students),
            "class_average": round(sum(s.average for s in students) / len(students), 2),
            "topper": self.ranked()[0].to_dict(),
            "grades": dict(grades),
            "courses": dict(courses),
        }

    # --- generator-powered bulk add -----------------------------------
    @timed
    def seed(self, count):
        """Add `count` random students, consuming the generator lazily."""
        next_id = 1000
        while f"S{next_id}" in self._students:
            next_id += 1
        added = 0
        for student in generate_students(count, start_id=next_id):
            self._students[student.student_id] = student
            added += 1
        self.save()
        return added
