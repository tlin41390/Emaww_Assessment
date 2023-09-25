import redis
import json
import xml.etree.ElementTree as ET
import argparse

def main():
    #Parse the arguments
    parser = argparse.ArgumentParser(description="Process XML and store data in Redis.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Print all keys saved to Redis")
    parser.add_argument("xml_path", help="Path to the XML file")
    args = parser.parse_args()
    
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
        
    if args.verbose:
        all_keys = redis_client.keys('*')
        print("All keys saved in Redis:")
        for key in all_keys:
            print(key)
        
if __name__ == "__main__":
    main()