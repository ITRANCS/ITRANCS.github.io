import json


with open('stv.json','r') as f:
    stv = json.load(f)

keys = list(stv.keys())

num = int(len(keys)/3)

i = 0

stv1 = {}
stv2 = {}
stv3 = {}

for key in stv:
    if i < num:
        stv1[key] = stv[key]
    elif i >=num and i < 2*num:
        stv2[key] = stv[key]
    else:
        stv3[key] = stv[key]
    i+=1

with open('stv1.json','w') as f:
    json.dump(stv1,f)

with open('stv2.json','w') as f:
    json.dump(stv2,f)

with open('stv3.json','w') as f:
    json.dump(stv3,f)



































