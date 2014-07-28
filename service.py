from flask import (
		Flask,
		redirect,
		render_template,
		request,
		send_file,
		url_for,
	)
from deferredvotes import *
from sampleData import genData
import sys

if len(sys.argv) < 2:
	print "usage: %s <database>" % (sys.argv[0])
	exit(1)
set_database(sys.argv[1])

app = Flask(__name__)

vote_fields = ("first", "last", "vote", "defer_first", "defer_last")
data_fields = ("placeholder")

@app.route("/")
def graph():
    return render_template('index.html', src="data")

@app.route("/sample")
def samplegraph():
    return render_template('index.html', src="sampledata")

@app.route("/<issue_hash>/form", methods=['GET', 'POST'])
def form(issue_hash):
    if request.method == 'POST':
		if all([k in request.form for k in vote_fields]):
			vote_id = get_user_id(request.form['first'], request.form['last'])
			defer_id = get_user_id(request.form['defer_first'], request.form['defer_last'])
			issue_id = id_from_hash(issue_hash)
			vote = request.form['vote']

			if submit_vote(vote_id, defer_id, issue_id, vote):
				return redirect(url_for("graph"))
    return send_file('templates/form.html')

@app.route("/data")
def data():
    print(str(get_json()))
    return get_json()

@app.route("/sampledata")
def sampledata():
    return genData()

if __name__ == "__main__":
    app.run(debug=True)
