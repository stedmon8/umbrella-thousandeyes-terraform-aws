import requests
import json


response = requests.post('https://management.api.umbrella.com/auth/v2/oauth2/token', auth=('XXXXX', 'XXXXXX'))

token_dict = json.loads(response.content)
token = token_dict['access_token'] 
authtok = "Bearer" + " " + token
with open('topwebsites.txt', 'w') as f:

    

    url = 'https://reports.api.umbrella.com/v2/organizations/orgID/top-destinations/dns?from=-1days&to=now&limit=10&offset=0'
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8', 'Authorization': authtok}
    r = requests.get(url, headers=headers)

    r_content = r.content
    r_dict = json.loads(r_content)


    top_websites = r_dict['data']

    for website in top_websites:
        print(website['domain'])
        f.write(website['domain'])
        f.write('\n')

#print(top_websites)