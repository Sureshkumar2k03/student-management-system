"""File handling: save and load student data as JSON."""

import json
import os

from exceptions import StorageError
from models import Student

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "students.json")


def save_students(students, path=DATA_FILE):
    """Write an iterable of Student objects to disk (atomic replace)."""
    tmp_path = path + ".tmp"
    try:
        with open(tmp_path, "w", encoding="utf-8") as fh:
            json.dump([s.to_dict() for s in students], fh, indent=2)
        os.replace(tmp_path, path)
    except OSError as exc:
        raise StorageError(f"Could not save data: {exc}") from exc


def load_students(path=DATA_FILE):
    """Return a list of Student objects; an absent file means no students yet."""
    try:
        with open(path, "r", encoding="utf-8") as fh:
            raw = json.load(fh)
    except FileNotFoundError:
        return []
    except (OSError, json.JSONDecodeError) as exc:
        raise StorageError(f"Could not read data file: {exc}") from exc
    try:
        return [Student.from_dict(item) for item in raw]
    except (KeyError, TypeError) as exc:
        raise StorageError(f"Data file is corrupted: {exc}") from exc
