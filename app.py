import redis
import json
import xml.etree.ElementTree as ET
def main():
    #Get the xml file
    tree = ET.parse('config.xml')
    root = tree.getroot()
    subdomains = []
    
    #Find all the subdomains and add them to a list
    for item_elem in root.findall('.//subdomains/subdomain'):

        subdomain = item_elem.text.strip()
        subdomains.append(subdomain)
    
    #Convert the list to json and store it in redis
    subdomains_json = json.dumps(subdomains)

    redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
    redis_client.set('subdomains', subdomains_json)

    #Find all the cookies and add them to a dictionary and then to the database
    for cookie_elem in root.findall('.//cookies/cookie'):   
        cookie = cookie_elem.attrib
        key = "cookie:"+cookie['name']+":"+cookie['host']
        redis_client.set(key, cookie_elem.text.strip())
        
main()