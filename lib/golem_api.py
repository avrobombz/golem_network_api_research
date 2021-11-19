import requests,json
from concurrent.futures import ThreadPoolExecutor, as_completed

def running():
    r = requests.get('https://api.stats.golem.network/v1/network/computing')
    curr_running = json.loads(r.text)
    curr_running = curr_running['computing_now']
    return(curr_running)

    
def pull_all_nodes_jsonstore(pullfresh):    
    if pullfresh:
        url = 'https://api.stats.golem.network/v1/network/historical/nodes'
        r = requests.get(url)
        j = json.loads(r.text)

        with open('dump.json', 'w') as jsonfile:
            jsonfile.write(json.dumps(j,indent=4))
    else:
        with open('dump.json','r') as jsonfile:
            j = json.loads(jsonfile.read())
    return(j)

def filter_json_hasearnings(j):

    keylist = []

    try: 
        for i, dictionary in enumerate(j):
            if(dictionary['online'] == True
                and dictionary['earnings_total'] != None 
                and float(dictionary['earnings_total']) > 0
                ):
                keylist.append(i)
    except:
        pass

    node_id_list = []
    for i in range(len(keylist)):
        node_id_list.append(j[keylist[i]]['node_id'])
    
    return(node_id_list,keylist)

def create_url_list(node_id_list,keylist):
#https://api.stats.golem.network/v1/provider/node/:yagna_id/activity
    #url_l = []
    d ={}
    for i in range(len(keylist)):
        node_id = node_id_list[i]        
        url = f'https://api.stats.golem.network/v1/provider/node/{node_id}/activity'
        d[node_id] = url
        #url_l.append(d)
    return d

def request(url,node_id):
    l = []
    d = {}
    r = requests.get(url)
    j = json.loads(r.text)
    try:
        check = j['data']['result'][0]['values']
        lengthcheck = len(check)-1
        d['node_id'] = node_id
        d['running'] = check[lengthcheck][1]
        l.append(d)
    except:
        pass

    with open('running.json', 'wa') as jsonfile:
        jsonfile.write(json.dumps(l,indent=4))

def runner(d):
    threads = []
    with ThreadPoolExecutor(max_workers=20) as executor:
        for node_id,url in d.items():
            threads.append(executor.submit(request,url,node_id))
            # print(url)
def open_runners_list():
    with open('running.json','r') as jsonfile:
        d = json.loads(jsonfile.read())
    return d