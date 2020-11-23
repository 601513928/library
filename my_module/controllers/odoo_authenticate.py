from xmlrpc import client

server_url = "http://localhost:8069"
db_name = 'library'
username = 'admin'
password = 'admin'
common = client.ServerProxy('%s/xmlrpc/2/common' % server_url)
user_id = common.authenticate(db_name, username, password, {})

print(common.version())
if user_id:
    print("Success: User id is ", user_id)
else:
    print("Failed: wrong credentials")