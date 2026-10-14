"""Console menu (functions): works on top of StudentManager."""

from exceptions import StudentError
from manager import StudentManager


def read_marks(text):
    """Parse 'Python=80, Maths=70' into {'Python': 80, 'Maths': 70}."""
    marks = {}
    for part in filter(None, (p.strip() for p in text.split(","))):
        subject, _, score = part.partition("=")
        marks[subject.strip()] = score.strip()
    return marks


def print_students(students):
    if not students:
        print("  (no students)")
        return
    for s in students:
        print("  " + str(s))


def add_student(mgr):
    s = mgr.add(input("ID: "), input("Name: "), input("Age: "), input("Course: "),
                read_marks(input("Marks (e.g. Python=80, Maths=70): ")))
    print(f"  Added {s.name}")


def update_student(mgr):
    sid = input("ID to update: ")
    old = mgr.get(sid)
    name = input(f"Name [{old.name}]: ") or old.name
    age = input(f"Age [{old.age}]: ") or old.age
    course = input(f"Course [{old.course}]: ") or old.course
    raw = input("Marks (blank = keep): ")
    mgr.update(sid, name, age, course, read_marks(raw) if raw.strip() else None)
    print("  Updated.")


def delete_student(mgr):
    print(f"  Deleted {mgr.delete(input('ID to delete: ')).name}")


def show_stats(mgr):
    st = mgr.stats()
    print(f"  Students: {st['count']}  Class average: {st['class_average']}")
    if st["topper"]:
        print(f"  Topper: {st['topper']['name']} ({st['topper']['average']})")
    print(f"  Grades: {st['grades']}")


MENU = """
===== Student Management System =====
1. Add student      2. List all       3. Search
4. Update           5. Delete         6. Statistics
7. Generate sample students           0. Exit
"""


def run():
    mgr = StudentManager()
    actions = {
        "1": add_student,
        "2": lambda m: print_students(m.all()),
        "3": lambda m: print_students(m.search(input("Search: "))),
        "4": update_student,
        "5": delete_student,
        "6": show_stats,
        "7": lambda m: print(f"  Added {m.seed(int(input('How many: ')))} students"),
    }
    while True:
        print(MENU)
        choice = input("Choose: ").strip()
        if choice == "0":
            print("Goodbye!")
            break
        action = actions.get(choice)
        if action is None:
            print("  Invalid choice.")
            continue
        try:
            action(mgr)
        except StudentError as exc:
            print(f"  Error: {exc}")
        except ValueError:
            print("  Error: please enter a valid number.")
