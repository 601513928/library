from xmlrpc import client

server_url = 'http://localhost:8069'
db_name = 'library'
username = 'admin'
password = 'admin'
common = client.ServerProxy('%s/xmlrpc/2/common' % server_url)
user_id = common.authenticate(db_name, username, password, {})
models = client.ServerProxy('%s/xmlrpc/2/object' % server_url)

if user_id:
    book_id = models.execute_kw(db_name, user_id, password, 'mylibrary.book', 'create', [{'name': 'New Book', 'date_release': '2020-01-01','state': 'draft', 'pages': 10}])
    print("Create book :", book_id)
    models.execute_kw(db_name, user_id, password, 'mylibrary.book', 'make_available', [[book_id]])

    book_data = models.execute_kw(db_name, user_id, password, 'mylibrary.book', 'read',[[book_id] ,['name', 'state']])
    print('Book state after method call:', book_data[0]['state'])
else:
    print('Wrong credentials')
