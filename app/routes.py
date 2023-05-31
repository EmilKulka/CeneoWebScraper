from app import app
from flask import Flask, render_template


@app.route("/name", defaults={"name":"Anonim"})
@app.route("/name/<name>")
def name(name):
    return f"Hello {name}"

@app.route("/")
def main_page():
    return render_template("index.html")

@app.route("/Ekstrakcja")
def extraction():
    return render_template("extraction.html")

@app.route("/Autor")
def author():
    return render_template("author.html")

@app.route("/Lista_produktów")
def product_list():
    return render_template("product_list.html")