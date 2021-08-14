import json
import geoip2.database
from iso3166 import countries
    
with open("stv.json",'r') as load_f:
    res1 = json.load(load_f)
with open("sn.json",'r') as load_f:
    res2 = json.load(load_f)
sn2 = {}
for src in res2:
    try:
        iso = countries.get(src).alpha3
    except:
        continue
    data = []
    for c in res2[src]:
        try:
            isocode = countries.get(c).alpha3
        except:
            continue
        data.append({'code':isocode,'value':res2[src][c]})
    sn2[iso] = data
stv2 = {}
for key in res1:
    c1,c2 = key.split('-')
    try:
        iso1 = countries.get(c1).alpha3
    except:
        continue
    try:
        iso2 = countries.get(c2).alpha3
    except:
        continue
    for c in res1[key]:
        try:
            isocode = countries.get(c).alpha3
        except:
            continue
        data.append({'code':isocode,'value':res1[key][c]})  
    stv2[iso1+'-'+iso2] = data

with open('sn2.json','w') as f:
    json.dump(sn2,f)

with open('stv2.json','w') as f:
    json.dump(stv2,f)



































