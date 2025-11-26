"""Student Grade Analyzer

Program allows adding students, grades, generating reports about them,
and finding top performer among students."""

students_list = []


def add_new_student():
    """Add a new student to the students_list."""
    student_name = input("Enter student name: ").strip()
    if not student_name:
        print("Invalid student name.")
        return

    for student in students_list:
        if student["name"] == student_name:
            print(f"Student {student_name} already exists.")
            return

    students_list.append({
        "name": student_name,
        "grades": []
    })
    print(f"Student {student_name} added.")


def add_new_grade():
    """Add grades to an existing student."""
    current_name = input("Enter student name: ")
    for student in students_list:
        if student["name"] == current_name:
            print("Enter the grades (type 'done' to finish):")
            while True:
                grade_input = input()
                if grade_input.lower() == "done":
                    print("Grades added.")
                    return
                try:
                    grade = int(grade_input)
                    if grade < 0 or grade > 100:
                        print("Invalid grade. Must be 0–100.")
                        continue
                except ValueError:
                    print("Invalid input. Enter a number from 0 to 100, or 'done'.")
                    continue
                student["grades"].append(grade)
            return
    print(f"Student {current_name} doesn't exist.")


def avg(grades: list) -> float | None:
    """Calculate average of a list of grades.

    Returns None if the list is empty.
    """
    try:
        return sum(grades) / len(grades)
    except ZeroDivisionError:
        return None


def student_report():
    """Print report for all students and overall statistics."""
    if not students_list:
        print("No students found.")
        return

    all_grades = []
    max_average = None
    min_average = None

    for student in students_list:
        average_grade = avg(student["grades"])

        if average_grade is None:
            print(f"{student['name']}'s average grade is N/A.")
        else:
            print(f"{student['name']}'s average grade is {average_grade:.2f}.")
            max_average = max(max_average or average_grade, average_grade)
            min_average = min(min_average or average_grade, average_grade)

        all_grades.extend(student["grades"])

    if not all_grades:
        print("No grades found.")
        return

    overall_average = sum(all_grades) / len(all_grades)
    if max_average is not None:
        print(f"Max average: {round(max_average, 1)}")
        print(f"Min average: {round(min_average, 1)}")
    print(f"Overall average: {round(overall_average, 1)}")


def best_student():
    """Find and print the student with the highest average grade."""
    if not students_list:
        print("No students found.")
        return

    students_with_grades = [s for s in students_list if s["grades"]]
    if not students_with_grades:
        print("No students with any grades found.")
        return

    top_student = max(students_with_grades, key=lambda s: avg(s["grades"]))
    top_avg = avg(top_student["grades"])
    print(f"The student with the highest average is {top_student['name']} "
          f"with a grade of {round(top_avg, 1)}.")


def main():
    """Menu loop for the Student Grade Analyzer."""
    while True:
        print(
            "\n--- Student Grade Analyzer ---\n"
            "1. Add a new student\n"
            "2. Add grades for a student\n"
            "3. Generate a full report\n"
            "4. Find the top student\n"
            "5. Exit the program\n"
        )
        try:
            option = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid input. Please enter a number in range 1-5.")
            continue

        match option:
            case 1:
                add_new_student()
            case 2:
                add_new_grade()
            case 3:
                student_report()
            case 4:
                best_student()
            case 5:
                print("Exiting program.")
                break
            case _:
                print("Invalid choice. Enter a number from 1 to 5.")


if __name__ == "__main__":
    main()

