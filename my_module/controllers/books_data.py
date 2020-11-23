from xmlrpc import client


server_url = 'http://localhost:8069'
db_name = 'library'
username = 'admin'
password = 'admin'
common = client.ServerProxy('%s/xmlrpc/2/common' % server_url)
user_id = common.authenticate(db_name, username, password, {})
models = client.ServerProxy('%s/xmlrpc/2/object' % server_url)

if user_id:
    search_domain = ['|', ['name', 'ilike', 'odoo'], ['name', 'ilike', 'sql']]
    #search_domain = []
    #替代下面的方式实现
    books_data = models.execute_kw(db_name, user_id, password, 'mylibrary.book', 'search_read', [search_domain, ['name', 'data_release']] ,{'limit': 5})
    print("Books data:", books_data)
    # books_ids = models.execute_kw(db_name, user_id, password, 'mylibrary.book', 'search', [search_domain], {'limit':5})
    # print('Books ids found:', books_ids)

    # books_data = models.execute_kw(db_name, user_id, password, 'mylibrary.book', 'read', [books_ids, ['name', 'data_release']])
    # print("Books data:", books_data)
else:
    print('Wrong credentials')
