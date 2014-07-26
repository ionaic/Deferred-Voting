from flask import Flask, send_file

app = Flask(__name__)

@app.route("/")
def graph():
    return send_file('templates/index.html')

@app.route("/form")
def form():
    return send_file('templates/form.html')

@app.route("/data")
def data():
    return "this will be the data page"

if __name__ == "__main__":
    app.run(debug=True)
