from flask import Flask, send_file, request
from deferredvotes import *

app = Flask(__name__)

vote_fields = ("name", "vote", "defer")
data_fields = ("placeholder")

@app.route("/")
def graph():
    return send_file('templates/index.html')

@app.route("/form")
def form():
    #if request.method == 'POST':
    #    if all([k in request.form for k in vote_fields]):
    #        submit_vote(*[request.form[k] for k in vote_fields])
    #        return send_file('templates/index.html')
    #else:
    return send_file('templates/form.html')

@app.route("/data", methods=['GET', 'POST'])
def data():
    if request.method == 'POST':
        if all([k in request.form for k in vote_fields]):
            submit_vote(*[request.form[k] for k in vote_fields])
            return send_file('templates/index.html')
    else:
        5
    return "this will be the data page"

if __name__ == "__main__":
    app.run(debug=True)
