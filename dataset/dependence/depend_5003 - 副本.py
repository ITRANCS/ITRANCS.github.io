import json
import geoip2.database
from iso3166 import countries

clist = []

with open("sn.json",'r') as load_f:
    res2 = json.load(load_f)

for src in res2:
    if src not in clist:
        clist.append(src)
    for des in res2[src]:
        if des not in clist:
            clist.append(des)

dic = {}
rev = {}
for c in clist:
    try:
        iso = countries.get(c).alpha3
    except:
        continue
    dic[c] = iso
    rev[iso] = c

with open('dic.json','w') as f:
    json.dump(dic,f)

with open('rev.json','w') as f:
    json.dump(rev,f)





























