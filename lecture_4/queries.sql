-- tables dropping to avoid accumulation of records
DROP TABLE IF EXISTS grades;
DROP TABLE IF EXISTS students;

CREATE TABLE students (
    id INTEGER PRIMARY KEY,
    full_name TEXT NOT NULL,
    birth_year INTEGER NOT NULL
);

CREATE TABLE grades (
    id INTEGER PRIMARY KEY,
    student_id INTEGER NOT NULL REFERENCES students(id),
    subject TEXT NOT NULL,
    grade INTEGER CHECK (grade => 0 AND grade <= 100)
);

--inserting the given records
INSERT INTO students (full_name, birth_year)
VALUES 
('Alice Johnson', 2005),
('Brian Smith', 2004),
('Carla Reyes', 2006),
('Daniel Kim', 2005),
('Eva Thompson', 2003),
('Felix Nguyen', 2007),
('Grace Patel', 2005),
('Henry Lopez', 2004),
('Isabella Martinez', 2006);

INSERT INTO grades (student_id, subject, grade)
VALUES
(1, 'Math', 88),
(1, 'English', 92),
(1, 'Science', 85),
(2, 'Math', 75),
(2, 'History', 83),
(2, 'English', 79),
(3, 'Science', 95),
(3, 'Math', 91),
(3, 'Art', 89),
(4, 'Math', 84),
(4, 'Science', 88),
(4, 'Physical Education', 93),
(5, 'English', 90),
(5, 'History', 85),
(5, 'Math', 88),
(6, 'Science', 72),
(6, 'Math', 78),
(6, 'English', 81),
(7, 'Art', 94),
(7, 'Science', 87),
(7, 'Math', 90),
(8, 'History', 77),
(8, 'Math', 83),
(8, 'Science', 80),
(9, 'English', 96),
(9, 'Math', 89),
(9, 'Art', 92);

--indexes for every field with "where", "join" or "order" usage
CREATE INDEX idx_students_full_name ON students (full_name);
CREATE INDEX idx_students_birth_year ON students (birth_year);

CREATE INDEX idx_grades_student_id ON grades (student_id);
CREATE INDEX idx_grades_subject ON grades (subject);
CREATE INDEX idx_grades_grade ON grades (grade);

--1. find all grades for a specific student (Alice Johnson)
SELECT * 
    FROM grades
    JOIN students 
    ON grades.student_id = students.id 
    WHERE students.full_name = 'Alice Johnson';

--2. Calculate the average grade per student
 SELECT students.full_name, AVG(grades.grade) AS avg_grade
    FROM grades 
    JOIN students ON grades.student_id = students.id
    GROUP BY students.id;

--3. All students born after 2004
SELECT * FROM students WHERE birth_year > 2004;

--4. the average grade for all subjects
SELECT subject, AVG(grade) as average_grade
    FROM grades
    GROUP BY subject;

--5. Top 3 students with the highest average grades
 SELECT students.full_name, AVG(grades.grade) AS avg_grade
    FROM grades 
    JOIN students ON grades.student_id = students.id
    GROUP BY students.id
    ORDER BY avg_grade DESC
    LIMIT 3;

--6. All students who have scored below 80 in any subject
 SELECT DISTINCT students.full_name
    FROM grades 
    JOIN students ON grades.student_id = students.id
    WHERE grades.grade < 80;