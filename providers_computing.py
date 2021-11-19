import requests, json, math, time, datetime
from lib import golem_api#, scrape

begin_time = datetime.datetime.now()

pullfresh = True #set to true if you wish to pull new node data from golem network

# Pull # of nodes currently running
currently_running = print(golem_api.running())

# Pull all nodes and store in jsonfile/memory
all_nodes = golem_api.pull_all_nodes_jsonstore(pullfresh)

# filter all_nodes down to only online nodes and have earnings
# store node_id_list, and key_list for all_nodes

stage1 = golem_api.filter_json_hasearnings(all_nodes)
node_id_list = stage1[0]
keylist = stage1[1]
#clear memory
stage1=[]

#create a url list for the threading
url_l = golem_api.create_url_list(node_id_list,keylist)

with open('dump2.json', 'w') as jsonfile:
    jsonfile.write(json.dumps(url_l,indent=4))

#find list of active nodes with a task
golem_api.runner(url_l)


endtime = datetime.datetime.now() - begin_time
print(endtime)
#######





# keylist = []
# for i, dictionary in enumerate(d):
#     if(dictionary['running'] == '1'
#         ):
#         keylist.append(i)

# node_list = []
# for i in range(len(keylist)):
#     node_list.append(d[keylist[i]]['node_id'])

# with open ('dump.json','r') as jsonfile:
#     dump = json.loads(jsonfile.read())

# dumpkeys = []

# try: 
#     for i, dictionary in enumerate(dump):
#         if(dictionary['node_id'] in node_list
#             ):
#             dumpkeys.append(i)
# except:
#     pass
# print(f'Currently Running : {curr_running} | # of records in dump:running {len(node_id_list)}:{len(dumpkeys)}')
# dictresults = {}
# for i in dumpkeys:
#     header = dump[i]['data']['golem.node.id.name'] #    "data""golem.node.id.name"
#     sub_d = {}
#     sub_d['node_id'] = dump[i]['node_id']
#     sub_d['earnings_total'] = dump[i]['earnings_total'] #    "earnings_total"
#     sub_d['CPU_Threads'] = dump[i]['data']['golem.inf.cpu.threads'] #    "data""golem.inf.cpu.threads"
#     sub_d['Memory_GB'] = dump[i]['data']['golem.inf.mem.gib'] #     "data""golem.inf.mem.gib"
#     sub_d['Memory_GB'] = dump[i]['data']['golem.inf.storage.gib'] #    "data""golem.inf.storage.gib"
#     dictresults[header] = sub_d

# with open('runner_info.json','w') as dumpfile:
#     json.dump(dictresults, dumpfile, indent=4)

# endtime = datetime.datetime.now() - begin_time
# print(endtime)