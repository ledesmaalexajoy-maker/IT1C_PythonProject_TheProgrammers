# IT1C_PythonProject_TheProgrammers
Student Management System in Python

├── source/main.py
├── documentation/pseudocode.txt
├── documentation/logic_explanation.txt
├── images/screenshot1.png
├── images/flowchart.png
└── README.md

import sqlite3

def create_table():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS students
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT, course TEXT, year INTEGER)''')
    conn.commit()
    conn.close()

def add_student():
    name = input("Name: "); course = input("Course: "); year = input("Year: ")
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute("INSERT INTO students (name, course, year) VALUES (?,?,?)", (name, course, year))
    conn.commit(); conn.close()
    print("Added!")

def view_students():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    for row in c.execute("SELECT * FROM students"):
        print(row)
    conn.close()

def main():
    create_table()
    while True:
        print("\n1.Add 2.View 3.Exit")
        choice = input("Choice: ")
        if choice=='1': add_student()
        elif choice=='2': view_students()
        else: break

if __name__ == "__main__": main()

BEGIN
  CREATE table
  WHILE True:
    Show menu
    IF choice=1: Add student
    IF choice=2: View students
    IF choice=3: Exit
END

# IT1C Python Project - The Programmers
Members: Alexa Joy Ledesma, Khecy lovely Asis, Lorie Grace Palasigue, Isaiah Natividad, Li Andrey Mampay, Lemar Eleazar
Section: BSIT 1C

Run: python main.py sa /source folder
![Flowchart](images/flowchart.png)
![Screenshot](images/screenshot1.png)
