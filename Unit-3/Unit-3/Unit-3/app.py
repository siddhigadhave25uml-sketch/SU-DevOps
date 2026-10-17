from flask import Flask, render_template, request, redirect, url_for, flash
from database import get_db, init_db

app = Flask(__name__)
app.config["SECRET_KEY"] = "replace-this-development-key"

@app.before_request
def prepare_database():
    init_db()

@app.route("/")
def index():
    db = get_db()
    stats = {
        "books": db.execute("SELECT COUNT(*) FROM books").fetchone()[0],
        "borrowers": db.execute("SELECT COUNT(*) FROM borrowers").fetchone()[0],
        "loans": db.execute("SELECT COUNT(*) FROM loans WHERE returned_on IS NULL").fetchone()[0],
        "overdue": db.execute("SELECT COUNT(*) FROM loans WHERE returned_on IS NULL AND due_on < date('now')").fetchone()[0],
    }
    return render_template("index.html", stats=stats)

@app.route("/books", methods=["GET", "POST"])
def books():
    db = get_db()
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        author = request.form.get("author", "").strip()
        isbn = request.form.get("isbn", "").strip()
        copies = request.form.get("copies", "1")
        if not title or not author or not isbn:
            flash("Title, author, and ISBN are required.")
        else:
            try:
                copies = int(copies)
                if copies < 1:
                    raise ValueError
                db.execute("INSERT INTO books (title, author, isbn, total_copies, available_copies) VALUES (?, ?, ?, ?, ?)",
                           (title, author, isbn, copies, copies))
                db.commit()
                flash("Book added.")
                return redirect(url_for("books"))
            except ValueError:
                flash("Copies must be a positive whole number.")
            except Exception:
                db.rollback()
                flash("Could not add book. The ISBN may already exist.")
    rows = db.execute("SELECT * FROM books ORDER BY id DESC").fetchall()
    return render_template("books.html", books=rows)

@app.route("/borrowers", methods=["GET", "POST"])
def borrowers():
    db = get_db()
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        if not name or not email:
            flash("Name and email are required.")
        else:
            try:
                db.execute("INSERT INTO borrowers (name, email) VALUES (?, ?)", (name, email))
                db.commit()
                flash("Borrower registered.")
                return redirect(url_for("borrowers"))
            except Exception:
                db.rollback()
                flash("Could not register borrower. Email may already be registered.")
    rows = db.execute("SELECT * FROM borrowers ORDER BY id DESC").fetchall()
    return render_template("borrowers.html", borrowers=rows)

@app.route("/loans", methods=["GET", "POST"])
def loans():
    db = get_db()
    if request.method == "POST":
        try:
            book_id = int(request.form["book_id"])
            borrower_id = int(request.form["borrower_id"])
            due_on = request.form["due_on"]
            book = db.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()
            if not book or book["available_copies"] < 1:
                flash("That book has no available copies.")
            else:
                db.execute("INSERT INTO loans (book_id, borrower_id, due_on) VALUES (?, ?, ?)",
                           (book_id, borrower_id, due_on))
                db.execute("UPDATE books SET available_copies = available_copies - 1 WHERE id = ?", (book_id,))
                db.commit()
                flash("Loan recorded.")
                return redirect(url_for("loans"))
        except Exception:
            db.rollback()
            flash("Could not create loan. Check the selected book, borrower, and due date.")
    books_list = db.execute("SELECT id, title, available_copies FROM books WHERE available_copies > 0 ORDER BY title").fetchall()
    borrowers_list = db.execute("SELECT id, name FROM borrowers ORDER BY name").fetchall()
    rows = db.execute("""
        SELECT l.id, b.title AS book, br.name AS borrower, l.borrowed_on, l.due_on,
               l.returned_on, CASE WHEN l.returned_on IS NULL AND l.due_on < date('now') THEN 1 ELSE 0 END AS overdue
        FROM loans l JOIN books b ON b.id=l.book_id
        JOIN borrowers br ON br.id=l.borrower_id
        ORDER BY l.id DESC
    """).fetchall()
    return render_template("loans.html", loans=rows, books=books_list, borrowers=borrowers_list)

@app.route("/loans/<int:loan_id>/return", methods=["POST"])
def return_book(loan_id):
    db = get_db()
    loan = db.execute("SELECT * FROM loans WHERE id = ?", (loan_id,)).fetchone()
    if not loan:
        flash("Loan not found.")
    elif loan["returned_on"] is not None:
        flash("This book has already been returned.")
    else:
        db.execute("UPDATE loans SET returned_on = date('now') WHERE id = ?", (loan_id,))
        db.execute("UPDATE books SET available_copies = available_copies + 1 WHERE id = ?", (loan["book_id"],))
        db.commit()
        flash("Book returned.")
    return redirect(url_for("loans"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
