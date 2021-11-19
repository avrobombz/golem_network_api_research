import requests, json, math

pullfresh = False #set to true if you wish to pull new node data from golem network

if pullfresh:
    url = 'https://api.stats.golem.network/v1/network/historical/nodes'
    r = requests.get(url)
    j = json.loads(r.text)

    with open('dump.json', 'w') as jsonfile:
        jsonfile.write(json.dumps(j,indent=4))

with open('dump.json','r') as jsonfile:
    j = json.loads(jsonfile.read())

keylist = []

for i, dictionary in enumerate(j):
    if(dictionary['online'] == True 
        and dictionary['data']['golem.inf.cpu.threads'] >= 2 
        and dictionary['data']['golem.inf.cpu.threads'] <= 4 
        and dictionary['data']["golem.inf.mem.gib"] >= 3
        and dictionary['data']["golem.inf.mem.gib"] <= 4
         ):
        keylist.append(i)

#print(keylist)

cpu_price_list = []
for i in range(len(keylist)):
    x = float(j[keylist[i]]['data']['golem.com.pricing.model.linear.coeffs'][1])*10000
    cpu_price_list.append(x)

node_name_list = []
for i in range(len(keylist)):
    node_name_list.append(j[keylist[i]]['data']['golem.node.id.name'])

earnings_list = []
for i in range(len(keylist)):
    earnings_list.append(j[keylist[i]]['earnings_total'])

id_list = []
for i in range(len(keylist)):
    id_list.append(j[keylist[i]]['node_id'])

print(node_name_list)
print(cpu_price_list)
print(earnings_list)

url = "https://api.stats.golem.network/v1/provider/node/"

url2 = "/earnings/"

id_moneylist = []
for i in range(len(id_list)):
    r = requests.get(url + id_list[i] + url2 + '72')
    id = json.loads(r.text)
    id_moneylist.append(id['earnings'])

print(id_moneylist)