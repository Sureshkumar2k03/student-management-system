"""OOP model: the Student class."""

from utils import (assign_grade, calculate_average, calculate_total,
                   validate_basic, validate_marks)


class Student:
    def __init__(self, student_id, name, age, course, marks=None):
        name, age, course = validate_basic(name, age, course)
        self.student_id = str(student_id).strip()
        self.name = name
        self.age = age
        self.course = course
        self.marks = validate_marks(marks or {})

    # --- computed properties -------------------------------------------
    @property
    def total(self):
        return calculate_total(self.marks)

    @property
    def average(self):
        return calculate_average(self.marks)

    @property
    def grade(self):
        return assign_grade(self.average)

    # --- serialisation -------------------------------------------------
    def to_dict(self):
        return {
            "student_id": self.student_id,
            "name": self.name,
            "age": self.age,
            "course": self.course,
            "marks": self.marks,
            "total": self.total,
            "average": self.average,
            "grade": self.grade,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["student_id"], data["name"], data["age"],
                   data["course"], data.get("marks", {}))

    def __str__(self):
        return (f"{self.student_id:<8} {self.name:<20} {self.age:<4} "
                f"{self.course:<12} avg={self.average:<6} grade={self.grade}")

    def __repr__(self):
        return f"Student({self.student_id!r}, {self.name!r})"
