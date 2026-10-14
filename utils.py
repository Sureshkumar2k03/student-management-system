"""Reusable helper functions: validation and calculations."""

from exceptions import InvalidDataError, InvalidMarksError


def validate_marks(marks):
    """Return a clean {subject: float} dict or raise InvalidMarksError."""
    if not isinstance(marks, dict):
        raise InvalidMarksError("Marks must be a dictionary of subject -> score.")
    clean = {}
    for subject, score in marks.items():
        try:
            value = float(score)
        except (TypeError, ValueError):
            raise InvalidMarksError(f"Marks for '{subject}' must be a number.")
        if not 0 <= value <= 100:
            raise InvalidMarksError(f"Marks for '{subject}' must be between 0 and 100.")
        clean[str(subject).strip()] = value
    return clean


def validate_basic(name, age, course):
    """Validate name/age/course and return cleaned values."""
    name = str(name).strip()
    course = str(course).strip()
    if not name:
        raise InvalidDataError("Name cannot be empty.")
    if not course:
        raise InvalidDataError("Course cannot be empty.")
    try:
        age = int(age)
    except (TypeError, ValueError):
        raise InvalidDataError("Age must be a whole number.")
    if not 5 <= age <= 100:
        raise InvalidDataError("Age must be between 5 and 100.")
    return name, age, course


def calculate_total(marks):
    return sum(marks.values())


def calculate_average(marks):
    return round(sum(marks.values()) / len(marks), 2) if marks else 0.0


def assign_grade(average):
    if average >= 90:
        return "A+"
    if average >= 80:
        return "A"
    if average >= 70:
        return "B"
    if average >= 60:
        return "C"
    if average >= 50:
        return "D"
    return "F"
