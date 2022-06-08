from random import choice

#PROXY_LIST
with open('proxies.txt', 'r') as file_handle:
    GEONODS = file_handle.read().splitlines()

#USER_AGENTS
with open('browser_agents.txt', 'r') as file_handle:
    USER_AGENTS = file_handle.read().splitlines()

with open('block_dns.txt', 'r') as file_handle:
    BLOCK_DNS = file_handle.read().splitlines()

PROXY_USER = ""
PROXY_PASS = ""
GEONODE_DNS = choice(GEONODS)
USER_AGENT = choice(USER_AGENTS)
