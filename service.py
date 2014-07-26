from flask import Flask, send_file, request, render_template
from deferredvotes import *
from sampleData import genData

app = Flask(__name__)

vote_fields = ("name", "vote", "defer")
data_fields = ("placeholder")

@app.route("/")
def graph():
    return render_template('index.html', src="data")

@app.route("/sample")
def samplegraph():
    return render_template('index.html', src="sampledata")

@app.route("/form", methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        if all([k in request.form for k in vote_fields]):
            submit_vote(*[request.form[k] for k in vote_fields])
            return send_file('templates/index.html')
    return send_file('templates/form.html')

@app.route("/data")
def data():
    print(str(get_json()))
    #return send_file('graph.json')
    return get_json()

@app.route("/sampledata")
def sampledata():
    return genData()

if __name__ == "__main__":
    app.run(debug=True)
