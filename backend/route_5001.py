from flask import Flask, render_template, request, jsonify
from flask_cors import *
import json
import geoip2
import geoip2.database
from haversine import haversine, Unit
import os
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


def trans(parts):
    dic = {}
    coor = []
    iplist = []
    for part in parts:
        coor.append([float(part.split(',')[2]),float(part.split(',')[1])])
        iplist.append(part.split(',')[0])
    geojson = {
        'type': 'FeatureCollection',
        'features': [
            {
                'type': 'Feature',
                'geometry': {
                'type': 'LineString',
                'coordinates': coor
                }
            }
        ]
        }
    jsondata = {'status':'success','iplist':iplist,'geojson':geojson}
    return jsondata
as2geo = open('../dataset/as2geo/as2geo-2021.json','r')
as2geodic = json.loads(as2geo.readlines()[0].strip())
as2geo.close()
def asp2geo(aspath,src,des,readercity):
    coor = []
    aslist = []
    judge = True
    if isIP(src):
        try:
            response = readercity.city(src)
            lat = response.location.latitude
            lng = response.location.longitude
            coor.append([lng,lat])
            aslist.append(aspath[0])
        except:
            judge = False
    if judge == False or isIP(src) == False:
        maxnum = -1
        for p in as2geodic[aspath[0]]:
            if int(p[2])>maxnum:
                lat = p[0]
                lng = p[1]
        coor.append([lng,lat])
        aslist.append(aspath[0])
    for i in range(len(aspath)-1):
        as1 = aspath[i]
        as2 = aspath[i+1]
        if int(as1)<int(as2):
            if as1 in interdic:
                if as2 in interdic[as1]:
                    ps = interdic[as1][as2][0].split(',')
                    coor.append([float(ps[1]),float(ps[0])])
                    aslist.append(as1)
                    ps = interdic[as1][as2][1].split(',')
                    coor.append([float(ps[1]),float(ps[0])])
                    aslist.append(as2)
                    continue
        else:
            if as2 in interdic:
                if as1 in interdic[as2]:
                    ps = interdic[as2][as1][0].split(',')
                    coor.append([float(ps[1]),float(ps[0])])
                    aslist.append(as1)
                    ps = interdic[as2][as1][1].split(',')
                    coor.append([float(ps[1]),float(ps[0])])
                    aslist.append(as2)
                    continue
        try:
            mindis = 10000000000
            for p1 in as2geodic[as1]:
                for p2 in as2geodic[as2]:
                    loc1 = (float(p1[0]), float(p1[1]))
                    loc2 = (float(p2[0]), float(p2[1]))
                    dis = haversine(loc1,loc2)
                    if dis < mindis:
                        mindis = dis
                        minloc1 = loc1
                        minloc2 = loc2
            coor.append([minloc1[1],minloc1[0]])
            aslist.append(as1)
            coor.append([minloc2[1],minloc2[0]])
            aslist.append(as2)
        except:
            return {'status':'failed'}
    judge = True
    if isIP(des):
        try:
            response = readercity.city(des)
            lat = response.location.latitude
            lng = response.location.longitude
            coor.append([lng,lat])
            aslist.append(aspath[-1])
        except:
            judge = False
    if judge == False or isIP(des) == False:
        maxnum = -1
        for p in as2geodic[aspath[-1]]:
            if int(p[2])>maxnum:
                lat = p[0]
                lng = p[1]
        coor.append([lng,lat])
        aslist.append(aslist[-1])
    geojson = {
        'type': 'FeatureCollection',
        'features': [
            {
                'type': 'Feature',
                'geometry': {
                'type': 'LineString',
                'coordinates': coor
                }
            }
        ]
    }
    jsondata = {'status':'success','aslist':aslist,'geojson':geojson}
    return jsondata
        
interdic = {}
interdomainlink = open('../dataset/BGP/2021/interdomainlink.txt','r')
for line in interdomainlink:
    parts = line.strip().split(' ')
    if parts[0] not in interdic:
        interdic[parts[0]] = {}
        interdic[parts[0]][parts[1]] = [parts[2],parts[3]]
interdomainlink.close()

def getas(readerasn,year,ip):
    if year == '2020' or year == '2021':
        response = readerasn.asn(ip)
        return str(response.autonomous_system_number)
    else:
        isp = readerasn.name_by_addr(ip).split()
        asn = isp[0]
        return str(asn)


@app.route('/route',methods=['GET'])
def route():
    src = request.args.get('src', 0, type=str)
    des = request.args.get('des', 0, type=str)
    year = request.args.get('time', 0, type=str)
    jsondata = {'status':'failed'}
    a1 = isIP(src)
    a2 = isasn(src)
    a3 = isIP(des)
    a4 = isasn(des)
    dbcity = '../dataset/ip2geo/GeoLite2-City-'+year+'.mmdb'
    readercity = geoip2.database.Reader(dbcity)
    if year == '2020' or year == '2021':
        dbasn = '../dataset/ip2as/GeoLite2-ASN-'+year+'.mmdb'
        readerasn = geoip2.database.Reader(dbasn)
    else:
        dbasn = '../dataset/ip2as/GeoIPASNum-'+year+'.dat'
        readerasn = GeoIP.open(dbasn, GeoIP.GEOIP_STANDARD)
    if a1 == False and a2 == False:
        return jsonify(jsondata)
    if a3 == False and a4 == False:
        return jsonify(jsondata)
    if a1:
        try:
            srcas = getas(readerasn,year,src)
        except:
            return jsonify(jsondata)
    else:
        srcas = src[2:]
    if a3:
        try:
            desas = getas(readerasn,year,des)
        except:
            return jsonify(jsondata)
    else:
        desas = des[2:]
    #traceroute
    print('Finding traceroute file...')
    pvalue = -1
    temp = []
    if year == '2021':
        trtfile = open('../dataset/traceroute/2020/2020_1.txt','r')
    else:
        trtfile = open('../dataset/traceroute/'+year+'/'+year+'_1.txt','r')
    for line in trtfile:
        parts = line.strip().split(' ')
        if len(parts) < 2:
            continue
        ps2 = parts[-1].split(',')
        if desas != ps2[3]:
            continue
        for i in range(len(parts)-1):
            ps1 = parts[i].split(',')       
            if a1 and a3:
                if ps1[0].split('.')[0:3] == src.split('.')[0:3]\
                    and ps2[0].split('.')[0:3] == des.split('.')[0:3]:
                        pvalue = 4
                        jsondata = trans(parts)
                        print('Find traceroute result p-value=4')
                        trtfile.close()
                        return jsonify(jsondata)
            if pvalue < 3 and srcas == ps1[3]:
                pvalue = 3
                temp = parts
    if pvalue == 3:
        jsondata = trans(temp)
        print('Find traceroute result p-value=3')
        trtfile.close()
        return jsonify(jsondata)       
    #routetable
    print('Finding route table...')
    root = '../dataset/BGP/'+year+'/inference/'
    if os.path.exists(root+desas+'.txt'):
        file = open(root+desas+'.txt','r')
        dic = {}
        for line in file:
            parts = line.strip().split(' ')
            dic[parts[0]] = parts[1]
        file.close()
        if srcas in dic:
            aslist = []
            aslist.append(srcas)
            nextas = dic[srcas]
            while nextas != desas:
                aslist.append(nextas)
                nextas = dic[nextas]
            aslist.append(desas)
            print(aslist)
            jsondata = asp2geo(aslist,src,des,readercity)
            pvalue = 2
            print('Find route table result p-value=2')
            return jsonify(jsondata)
    #aspathinference
    print('Finding inference path...')
    root = '../dataset/BGP/'+year+'/path/'
    if os.path.exists(root+desas+'.txt'):
        file = open(root+desas+'.txt','r')
        dic = {}
        for line in file:
            parts = line.strip().split(' ')
            dic[parts[0]] = parts[1]
        file.close()
        if srcas in dic:
            aslist = []
            aslist.append(srcas)
            nextas = dic[srcas]
            while nextas != desas:
                aslist.append(nextas)
                nextas = dic[nextas]
            aslist.append(desas)
            print(aslist)
            jsondata = asp2geo(aslist,src,des,readercity)
            pvalue = 1
            print('Find inference path result p-value=1')
            return jsonify(jsondata)    

if __name__ == "__main__":
    app.run(host='127.0.0.1',port=5001)
