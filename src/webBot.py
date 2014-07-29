from flask import Flask
from flask import request
from bot import resolveAction
import xml.etree.ElementTree as ET


app = Flask(__name__)

@app.route("/", methods=['POST'])
def mainFunction():
    
    # Parse the parameters from the request POST data
    name    = request.form['name']
    pocket  = request.form['pocket'].split()
    choices = request.form['actions'].split('\n')
    stateXML= request.form['state']

    # Parse from XML
    stateXML = ET.fromstring(stateXML)

    # Ask for the next move
    ac = resolveAction(name,pocket,choices,stateXML)

    return ac

if __name__ == "__main__":
    app.run(debug=True)
