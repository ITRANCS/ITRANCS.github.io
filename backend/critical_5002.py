from flask import Flask, render_template, request, jsonify
from flask_cors import *
import json
import geoip2.database
from iso3166 import countries
app = Flask(__name__)
CORS(app, resources=r'/*')

namedic = ['degree','betweenness','closeness','eigenvector','flow']

@app.route('/')
@app.route('/index.html')

@app.route('/critical',methods=['GET'])
def search():
    name = request.args.get('name', 0, type=str)
    if name in namedic:
        file = open('../dataset/critical/2019_critical_node_rank_'+name+'.txt','r')
        dic = {}
        maxvalue = -1
        minvalue = 10000000
        for line in file:
            parts = line.strip().split(' ')
            dic[parts[0]] = float(parts[1])
            if float(parts[1]) > maxvalue:
                maxvalue = float(parts[1])
            elif float(parts[1]) < minvalue:
                minvalue = float(parts[1])
        file.close()
        for key in dic:
            dic[key] = (dic[key]-minvalue)/(maxvalue-minvalue)
        data = []
        for key in dic:
            try:
                isocode = countries.get(key).alpha3
                #print(isocode)
            except:
                continue
            data.append({'code':isocode,'value':dic[key]})
        jsondata = {'status':'success','data':data}
        #print(data)
        return jsondata
    
    
        

if __name__ == "__main__":
    app.run(host='127.0.0.1',port=5002)
