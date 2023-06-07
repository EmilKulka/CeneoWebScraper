from app import app
from flask import Flask, render_template, request, redirect, url_for


@app.route("/name", defaults={"name":"Anonim"})
@app.route("/name/<name>")
def name(name):
    return f"Hello {name}"

@app.route("/")

@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/extract", methods=["POST", "GET"])
def extract():
    if request.method == "POST":
        product_code = request.form.get("product_code")
        return redirect(url_for('product_site', code=product_code))
    return render_template("extraction.html")

@app.route("/author")
def author():
    return render_template("author.html")

@app.route("/product_list")
def product_list():
    return render_template("product_list.html")

@app.route("/product_site/<code>")
def product_site(code):
    return render_template("product_site.html", product_code=code)