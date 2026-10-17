from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from pathlib import Path

app = Flask(__name__)
app.secret_key = 'change-this-development-key'
DB_PATH = Path(__file__).with_name('students.db')

def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with db() as con:
        con.executescript('''
        CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, email TEXT, department TEXT, year TEXT);
        CREATE TABLE IF NOT EXISTS courses (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, code TEXT UNIQUE NOT NULL);
        CREATE TABLE IF NOT EXISTS attendance (id INTEGER PRIMARY KEY AUTOINCREMENT, student_id INTEGER NOT NULL, course_id INTEGER NOT NULL, date TEXT NOT NULL, status TEXT NOT NULL, FOREIGN KEY(student_id) REFERENCES students(id), FOREIGN KEY(course_id) REFERENCES courses(id));
        CREATE TABLE IF NOT EXISTS marks (id INTEGER PRIMARY KEY AUTOINCREMENT, student_id INTEGER NOT NULL, course_id INTEGER NOT NULL, score REAL NOT NULL, FOREIGN KEY(student_id) REFERENCES students(id), FOREIGN KEY(course_id) REFERENCES courses(id));
        ''')

@app.route('/')
def index():
    with db() as con:
        counts = {table: con.execute(f'SELECT COUNT(*) FROM {table}').fetchone()[0] for table in ('students','courses','attendance','marks')}
        students = con.execute('SELECT * FROM students ORDER BY id DESC LIMIT 5').fetchall()
    return render_template('index.html', counts=counts, students=students)

@app.route('/students', methods=['GET','POST'])
def students():
    with db() as con:
        if request.method == 'POST':
            name = request.form.get('name','').strip()
            if not name:
                flash('Student name is required.', 'error')
            else:
                con.execute('INSERT INTO students(name,email,department,year) VALUES(?,?,?,?)', (name, request.form.get('email','').strip(), request.form.get('department','').strip(), request.form.get('year','').strip()))
                con.commit(); flash('Student added successfully.', 'success'); return redirect(url_for('students'))
        rows = con.execute('SELECT * FROM students ORDER BY name').fetchall()
    return render_template('students.html', students=rows)

@app.post('/students/<int:student_id>/delete')
def delete_student(student_id):
    with db() as con:
        con.execute('DELETE FROM attendance WHERE student_id=?',(student_id,)); con.execute('DELETE FROM marks WHERE student_id=?',(student_id,)); con.execute('DELETE FROM students WHERE id=?',(student_id,)); con.commit()
    flash('Student deleted.', 'success'); return redirect(url_for('students'))

@app.route('/courses', methods=['GET','POST'])
def courses():
    with db() as con:
        if request.method == 'POST':
            name, code = request.form.get('name','').strip(), request.form.get('code','').strip().upper()
            if name and code:
                try:
                    con.execute('INSERT INTO courses(name,code) VALUES(?,?)',(name,code)); con.commit(); flash('Course added.', 'success')
                except sqlite3.IntegrityError: flash('That course code already exists.', 'error')
            else: flash('Course name and code are required.', 'error')
            return redirect(url_for('courses'))
        rows = con.execute('SELECT * FROM courses ORDER BY code').fetchall()
    return render_template('courses.html', courses=rows)

@app.route('/attendance', methods=['GET','POST'])
def attendance():
    with db() as con:
        if request.method == 'POST':
            try:
                con.execute('INSERT INTO attendance(student_id,course_id,date,status) VALUES(?,?,?,?)', (int(request.form['student_id']), int(request.form['course_id']), request.form['date'], request.form['status'])); con.commit(); flash('Attendance recorded.', 'success')
            except (ValueError, KeyError, sqlite3.IntegrityError): flash('Please enter valid attendance details.', 'error')
            return redirect(url_for('attendance'))
        students = con.execute('SELECT * FROM students ORDER BY name').fetchall(); courses = con.execute('SELECT * FROM courses ORDER BY code').fetchall()
        rows = con.execute('SELECT a.*, s.name student_name, c.code course_code FROM attendance a JOIN students s ON s.id=a.student_id JOIN courses c ON c.id=a.course_id ORDER BY a.date DESC, a.id DESC').fetchall()
    return render_template('attendance.html', students=students, courses=courses, records=rows)

@app.route('/marks', methods=['GET','POST'])
def marks():
    with db() as con:
        if request.method == 'POST':
            try:
                score = float(request.form['score'])
                if not 0 <= score <= 100: raise ValueError()
                con.execute('INSERT INTO marks(student_id,course_id,score) VALUES(?,?,?)', (int(request.form['student_id']), int(request.form['course_id']), score)); con.commit(); flash('Marks saved.', 'success')
            except (ValueError, KeyError, sqlite3.IntegrityError): flash('Enter valid marks between 0 and 100.', 'error')
            return redirect(url_for('marks'))
        students = con.execute('SELECT * FROM students ORDER BY name').fetchall(); courses = con.execute('SELECT * FROM courses ORDER BY code').fetchall()
        rows = con.execute('SELECT m.*, s.name student_name, c.code course_code FROM marks m JOIN students s ON s.id=m.student_id JOIN courses c ON c.id=m.course_id ORDER BY s.name').fetchall()
    return render_template('marks.html', students=students, courses=courses, records=rows)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
