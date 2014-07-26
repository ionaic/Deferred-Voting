from flask import Flask, send_file, request
from deferredvotes import *
from sampleData import genData

app = Flask(__name__)

vote_fields = ("name", "vote", "defer")
data_fields = ("placeholder")

@app.route("/")
def graph():
    return send_file('templates/index.html')

@app.route("/form", methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        if all([k in request.form for k in vote_fields]):
            submit_vote(*[request.form[k] for k in vote_fields])
            return send_file('templates/index.html')
    return send_file('templates/form.html')

@app.route("/data")
def data():
    get_json()
    return send_file('graph.json')

@app.route("/sampledata")
def sampledata():
    return genData()

if __name__ == "__main__":
    app.run(debug=True)
