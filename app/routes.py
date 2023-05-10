from app import app

@app.route("/name", defaults={"name":"Anonim"})
@app.route("/name/<name>")
def name(name):
    return f"Hello {name}"