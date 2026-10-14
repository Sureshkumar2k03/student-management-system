"""Generators: produce students lazily, one at a time."""

import random

from models import Student

FIRST = ["Arun", "Divya", "Karthik", "Meena", "Naveen", "Priya", "Ravi",
         "Sangeetha", "Vijay", "Lakshmi", "Harish", "Nandhini"]
LAST = ["Kumar", "Raj", "Devi", "Selvam", "Murugan", "Babu", "Pandian"]
COURSES = ["BCA", "BSc CS", "BCom", "MCA"]
SUBJECTS = ["Python", "Maths", "DBMS", "Web Tech"]


def generate_students(count, start_id=1000, seed=None):
    """Yield `count` random Student objects without building a list first."""
    rng = random.Random(seed)
    for i in range(count):
        yield Student(
            student_id=f"S{start_id + i}",
            name=f"{rng.choice(FIRST)} {rng.choice(LAST)}",
            age=rng.randint(18, 24),
            course=rng.choice(COURSES),
            marks={s: rng.randint(35, 100) for s in SUBJECTS},
        )


def iter_top_students(students, min_average):
    """Lazily yield only the students whose average meets the threshold."""
    for student in students:
        if student.average >= min_average:
            yield student
