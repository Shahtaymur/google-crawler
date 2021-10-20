import requests

username = "geonode_uMZlIrin1i-autoReplace-True"
password = "b35b456b-90f7-4d88-88c4-b1bae00143a6"
GEONODE_DNS = "rotating-residential.geonode.com:9000"
urlToGet = "http://ip-api.com/json"
proxy = {"http":"http://{}:{}@{}".format(username, password, GEONODE_DNS)}
r = requests.get(urlToGet , proxies=proxy)

print("Response:\n{}".format(r.text))