from flask import Flask, render_template, request, jsonify
from flask_cors import *
import json
import geoip2.database
from iso3166 import countries
app = Flask(__name__)
CORS(app, resources=r'/*')


@app.route('/')
@app.route('/index.html')

@app.route('/depend',methods=['GET'])
def depend():
    srccountry = request.args.get('src', 0, type=str)
    descountry = request.args.get('des', 0, type=str)
    
    src = countries.get(srccountry).alpha2
    
    with open("../dataset/dependence/stv.json",'r') as load_f:
        res1 = json.load(load_f)
    with open("../dataset/dependence/sn.json",'r') as load_f:
        res2 = json.load(load_f)
    data = []
    if descountry == 'none':
        for c in res2[src]:
            try:
                isocode = countries.get(c).alpha3
            except:
                continue
            data.append({'code':isocode,'value':res2[src][c]})  
        jsondata = {'status':'success','data':data}
        return jsondata
    else:
        des = countries.get(descountry).alpha2
        key = src+'-'+des
        for c in res1[key]:
            try:
                isocode = countries.get(c).alpha3
            except:
                continue
            data.append({'code':isocode,'value':res1[key][c]})  
        jsondata = {'status':'success','data':data}
        return jsondata



    
    
        

if __name__ == "__main__":
    app.run(host='127.0.0.1',port=5003)
