

# Import requests for curl commands for API request
# Import Json to format data into Json 

import requests
import json

authtoken = "Bearer XXXXXX"
#Open text file with top applications URLs
with open('topwebsites.txt', 'r') as f:
    apps = f.read().splitlines()

#Create list variable ThousandEyes Canandian Agents
CA_AgentsIds = list()

#Send API request to get all ThousandEyes Agents in the world
url = "https://api.thousandeyes.com/v6/agents.json"
headers= {'Authorization' : authtoken }
resp = requests.get(url, headers=headers)

#TE API responds with a list of all agents
agentlist = resp.content 

#Take json content and load into a python dictionary
agentlist_dict = json.loads(agentlist)

#Structure dictionary to provide a list of all agents
agent_info = agentlist_dict['agents']
print(agent_info)
#Filter for only CA ThousandEyes agents. If the agent location is CA, take the agent ID and put it into my CanadaAgentsIDs variable list
for i in agent_info:
    if "Los Angeles" in i['location'] :
        agentid = i['agentId']
        CA_AgentsIds.append(agentid)
    if i['agentType'] == "Enterprise" :
        agentid = i['agentId']
        CA_AgentsIds.append(agentid)
print(CA_AgentsIds)



#For each app/website create a network agent to server ThousandEyes Test 
for i in apps:
    

    url = 'https://api.thousandeyes.com/v6/tests/agent-to-server/new.json'
    headers = {'content-type': 'application/json', 'Accept' : 'application/json', 'Authorization': authtoken }
    data = { "interval": 300,
            "agents": [],
            "testName": str(i) + " test",
            "server": str(i) ,
            "port": 80,
            "alertsEnabled": 0
        }

    
# Include all CA agents for these test
    for a in CA_AgentsIds:
        agent = {'agentId': a}
        data['agents'].append(agent)

    data = json.dumps(data)
    r = requests.post(url, headers=headers, data=data)
    
# Show repsonse codes
    print(r.content)
    print(json.dumps(data,indent=2))
