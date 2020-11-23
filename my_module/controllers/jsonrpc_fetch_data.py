import json
import requests
import random

server_url = 'http://localhost:8069'
db_name = 'library'
username = 'admin'
password = 'admin'

json_endpoint = "%s/jsonrpc" % server_url
headers = {"Content-Type": "application/json"}
def get_json_payload(service, method, *args):
    return json.dumps({
        "jsonrpc": "2.0",
        "method": 'call',
        "params": {
            "service": service,
            "method": method,
            "args": args
        },
        "id": random.randint(0, 100000000),
    })

payload = get_json_payload("common", "login", db_name, username, password)
response = requests.post(json_endpoint, data=payload, headers=headers)
user_id = response.json()['result']

if user_id:
    #搜索图书的id
    search_domain = ['|',['name', 'ilike', 'odoo'], ['name', 'ilike', 'sql']]
    # payload = get_json_payload("object", "execute_kw", db_name, user_id, password, 'mylibrary.book', 'search', [search_domain], {'limit': 5})
    # res = requests.post(json_endpoint, data=payload, headers=headers).json()
    # print('Book data:', res)
    # #为图书id 读取数据
    # payload = get_json_payload("object", "execute_kw", db_name, user_id, password, 'mylibrary.book', 'read', [res['result'], ['name', 'date_release']])
    # res = requests.post(json_endpoint, data=payload, headers=headers).json()
    # print('Books data:', res)

    #类似于XML-RPC可以使用search_read
    payload = get_json_payload("object", "execute_kw", db_name, user_id, password, 'mylibrary.book', 'search_read', [search_domain, ['name', 'date_release']], {'limit': 5})
    res = requests.post(json_endpoint, data=payload, headers=headers).json()
    print('Books data:', res)
else:
    print("Failed: wrong credentials")