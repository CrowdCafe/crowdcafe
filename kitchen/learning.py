import requests

url = 'https://api.github.com/repos/CrowdCafe/crowdcafe-ui-templates/contents'
headers = {'User-Agent': 'CrowdCafe'}

r = requests.get(url, headers = headers)

print r.json()