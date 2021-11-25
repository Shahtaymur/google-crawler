import os
import zipfile
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import time

PROXY_HOST = 'rotating-residential.geonode.com'  # rotating proxy or host
PROXY_PORT = 9000 # port
PROXY_USER = 'geonode_uMZlIrin1i' # username
PROXY_PASS = 'b35b456b-90f7-4d88-88c4-b1bae00143a6' # password


manifest_json = """
{
    "version": "1.0.0",
    "manifest_version": 2,
    "name": "Chrome Proxy",
    "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "<all_urls>",
        "webRequest",
        "webRequestBlocking"
    ],
    "background": {
        "scripts": ["background.js"]
    },
    "minimum_chrome_version":"22.0.0"
}
"""

background_js = """
var config = {
        mode: "fixed_servers",
        rules: {
        singleProxy: {
            scheme: "http",
            host: "%s",
            port: parseInt(%s)
        },
        bypassList: ["localhost"]
        }
    };

chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

function callbackFn(details) {
    return {
        authCredentials: {
            username: "%s",
            password: "%s"
        }
    };
}

chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
);
""" % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)


def get_chromedriver(use_proxy=False, user_agent=None):
    path = os.path.dirname(os.path.abspath(__file__))
    chrome_options = webdriver.ChromeOptions()
    if use_proxy:
        pluginfile = 'proxy_auth_plugin.zip'

        with zipfile.ZipFile(pluginfile, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)
        chrome_options.add_extension(pluginfile)
    if user_agent:
        chrome_options.add_argument('--user-agent=%s' % user_agent)
    driver = webdriver.Chrome(
        #os.path.join(path, 'chromedriver'),
        ChromeDriverManager().install(),
        chrome_options=chrome_options)
    return driver

def main():
    driver = get_chromedriver(use_proxy=True)
    while True:
        driver.get('http://www.google.com/')
        if not driver.title == "466 Too many requests":
            search_box = driver.find_element_by_name('q') #Search bar
            search_box.send_keys("what is my ip") #Type query
            search_box.submit()         #Hit Enter
            time.sleep(2)
            
            #driver.get('https://ipinfo.io/ip')
            print(driver.page_source)
            time.sleep(5)
        driver.close()

if __name__ == '__main__':
    main()