from flask import Flask, render_template, request, jsonify
from flask_cors import *
import json
import geoip2.database
app = Flask(__name__)
CORS(app, resources=r'/*')

import re

def isIP(s):
    p = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if p.match(s):
        return True
    else:
        return False
def isasn(s):
    if len(s)>2 and s[0:2] == 'AS':
        try:
            asn = int(s[2:])
        except:
            return False
        return True
    else:
        return False

@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')

dbcity = '../dataset/ip2geo/GeoLite2-City-2021.mmdb'
readercity = geoip2.database.Reader(dbcity)
as2geo = open('../dataset/as2geo/as2geo-2021.json','r')
as2geodic = json.loads(as2geo.readlines()[0].strip())
as2geo.close()
@app.route('/search',methods=['GET'])
def search():
    name = request.args.get('name', 0, type=str)
    if isIP(name):
        response = readercity.city(name)
        lat = response.location.latitude
        lng = response.location.longitude
        jsondata = {'type':'ip2geo','lat':lat,'lng':lng}
        return jsonify(jsondata)
    if isasn(name):
        asn = name[2:]
        if asn in as2geodic:
            jsondata = {'type':'as2geo','res':as2geodic[asn]}
            return jsonify(jsondata)
            
        

if __name__ == "__main__":
    app.run(host='127.0.0.1',port=5000)
