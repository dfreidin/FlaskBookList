from flask import Flask, render_template, request, redirect
from mysqlconnection import MySQLConnector
app = Flask(__name__)
mysql = MySQLConnector(app, "mybooks")
@app.route('/')
def index():
    books = mysql.query_db("SELECT id, title, author, DATE_FORMAT(created_at, '%b %D %Y') AS added_date FROM books;")
    return render_template('index.html', books=books)
@app.route("/add")
def add():
    return render_template("add.html")
@app.route("/add", methods=["POST"])
def procAdd():
    title = request.form["title"]
    author = request.form["author"]
    if len(title) < 1 or len(author) < 1:
        flash("Can't add a book without both Title and Author")
        return redirect("/")
    query = "INSERT INTO books (title, author, created_at, updated_at) VALUES(:title, :author, NOW(), NOW());"
    query_data = {"title": title, "author": author}
    res = mysql.query_db(query, query_data)
    print res
    return redirect("/")
@app.route("/destroy/<id>")
def destroy(id):
    books = mysql.query_db("SELECT title FROM books WHERE id = :id", {"id": id})
    if len(books) < 1:
        flash("Error, no book found with id {}".format(id))
        return redirect("/")
    return render_template("destroy.html", title=books[0]["title"], id=id)
@app.route("/destroy/<id>/delete")
def delete(id):
    query = "DELETE FROM books WHERE id = :id;"
    query_data = {"id": id}
    mysql.query_db(query, query_data)
    return redirect("/")
@app.route("/update/<id>")
def update(id):
    books = mysql.query_db("SELECT id, title, author FROM books WHERE id = :id", {"id": id})
    if len(books) < 1:
        flash("Error, no book found with id {}".format(id))
        return redirect("/")
    return render_template("update.html", book=books[0])
@app.route("/update", methods=["POST"])
def procUpdate():
    title = request.form["title"]
    author = request.form["author"]
    id = request.form["id"]
    query = "UPDATE books SET title = :title, author = :author, updated_at = NOW() WHERE id = :id"
    query_data = {"title": title, "author": author, "id": id}
    mysql.query_db(query, query_data)
    return redirect("/")
app.run(debug=True)