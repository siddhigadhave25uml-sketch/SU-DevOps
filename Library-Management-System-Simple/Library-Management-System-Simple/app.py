import os
from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "change-this-for-real-deployments")

def connect_db():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "library_user"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "library_db"),
        connection_timeout=5,
    )

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/books")
def books():
    try:
        conn = connect_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, title, author FROM books ORDER BY id DESC")
        books = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template("books.html", books=books)
    except Error:
        flash("Database unavailable. Please try again later.", "error")
        return render_template("books.html", books=[]), 503

@app.route("/add", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        author = request.form.get("author", "").strip()
        if not title or not author:
            flash("Enter both title and author.", "error")
            return render_template("add_book.html"), 400
        conn = None
        cursor = None
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO books (title, author) VALUES (%s, %s)", (title, author))
            conn.commit()
            flash("Book added successfully!", "success")
            return redirect(url_for("books"))
        except Error:
            if conn:
                conn.rollback()
            flash("Could not save the book. Check the database.", "error")
            return render_template("add_book.html"), 503
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    return render_template("add_book.html")

@app.route("/health")
def health():
    try:
        conn = connect_db()
        conn.close()
        return {"status": "ok"}, 200
    except Error:
        return {"status": "database unavailable"}, 503

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")))
