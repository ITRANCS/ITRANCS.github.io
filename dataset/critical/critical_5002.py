import json
import geoip2.database
from iso3166 import countries
namedic = ['degree','betweenness','closeness','eigenvector','flow']


for name in namedic:
    file = open('2019_critical_node_rank_'+name+'.txt','r')
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
        except:
            continue
        data.append({'code':isocode,'value':dic[key]})
    with open(name+'.json','w') as f:
        json.dump(data,f)
