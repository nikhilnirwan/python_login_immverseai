from distutils.log import debug
from routes.routes import app
from midlware.midleware import not_found

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    return not_found()
    

if __name__ == "__main__":
    app.run(debug=True)

