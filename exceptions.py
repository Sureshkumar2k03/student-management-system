"""Custom exceptions for the Student Management System."""


class StudentError(Exception):
    """Base class for all application errors."""


class StudentNotFoundError(StudentError):
    def __init__(self, student_id):
        super().__init__(f"Student with ID '{student_id}' was not found.")
        self.student_id = student_id


class DuplicateStudentError(StudentError):
    def __init__(self, student_id):
        super().__init__(f"Student with ID '{student_id}' already exists.")
        self.student_id = student_id


class InvalidMarksError(StudentError):
    """Raised when marks are not numbers between 0 and 100."""


class InvalidDataError(StudentError):
    """Raised when student data (name, age, course...) is invalid."""


class StorageError(StudentError):
    """Raised when saving or loading the data file fails."""
