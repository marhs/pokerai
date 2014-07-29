from flask import Flask
from flask import request
from bot import resolveAction
import xml.etree.ElementTree as ET


app = Flask(__name__)

@app.route("/", methods=['POST'])
def hello():
    

    name    = request.form['name']
    pocket  = request.form['pocket'].split()
    choices = request.form['actions'].split('\n')
    state   = request.form['state']

    root = ET.fromstring(state)
    ac = resolveAction(name,pocket,choices,root)

    return ac

if __name__ == "__main__":
    app.run(debug=True)
