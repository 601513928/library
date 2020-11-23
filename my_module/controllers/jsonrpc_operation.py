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
    #创建图书记录
    create_data = [
        {'name': 'Book 11', 'date_release': '2020-01-20', 'pages': 10},
        {'name': 'Book 12', 'date_release': '2020-01-20', 'pages': 10},
        {'name': 'Book 13', 'date_release': '2020-01-20', 'pages': 10},
        {'name': 'Book 14', 'date_release': '2020-10-10', 'pages': 10}
    ]

    payload = get_json_payload('object', 'execute_kw', db_name, user_id, password, 'mylibrary.book', 'create', [create_data])
    res = requests.post(json_endpoint, data=payload, headers=headers).json()
    print("Books created:", res)
    books_ids = res['result']

    #写入已有图书记录
    book_to_write = books_ids[1]
    write_data = {'name': 'Book 32'}
    payload = get_json_payload("object", "execute_kw", db_name, user_id, password, 'mylibrary.book', 'write', [book_to_write, write_data])
    res = requests.post(json_endpoint, data=payload, headers=headers).json()
    print("Books written:", res)

    #在已有图书记录中进行删除
    book_to_unlink = books_ids[2:]
    payload = get_json_payload("object", "execute_kw", db_name, user_id, password, 'mylibrary.book', 'unlink', [book_to_unlink])
    res = requests.post(json_endpoint, data=payload, headers=headers).json()
    print("Books deleted:", res)

else:
    print("Failed: wrong credentials")

