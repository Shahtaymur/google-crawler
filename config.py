from random import choice

#PROXY_LIST
with open('proxies.txt', 'r') as file_handle:
    GEONODS = file_handle.read().splitlines()

#USER_AGENTS
with open('browser_agents.txt', 'r') as file_handle:
    USER_AGENTS = file_handle.read().splitlines()

PROXY_USER = "geonode_uMZlIrin1i"
PROXY_PASS = "b35b456b-90f7-4d88-88c4-b1bae00143a6"
GEONODE_DNS = choice(GEONODS)
USER_AGENT = choice(USER_AGENTS)