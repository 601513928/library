from xmlrpc import client

server_url = 'http://localhost:8069'
db_name = 'library'
username = 'admin'
password = 'admin'
common = client.ServerProxy('%s/xmlrpc/2/common' % server_url)
user_id = common.authenticate(db_name, username, password, {})
models = client.ServerProxy('%s/xmlrpc/2/object' % server_url)

if user_id:
    #创建 book
    create_data = [
        {'name': 'Book one', 'release_date': '2019-01-16', 'pages': 10},
        {'name': 'Book two', 'release_date': '2019-02-16', 'pages': 10},
        {'name': 'Book three', 'release_date': '2019-03-16', 'pages': 10},
        {'name': 'Book four', 'release_date': '2019-05-16', 'pages': 10}
    ]

    books_ids = models.execute_kw(db_name, user_id, password, 'mylibrary.book', 'create', [create_data])
    print("Books created:", books_ids)

    #写入已经存在的记录
    book_to_write = books_ids[1]
    write_data = {'name': 'Books update'}
    written = models.execute_kw(db_name, user_id, password, 'mylibrary.book', 'write', [book_to_write, write_data])
    print("Books written:", written)

    #删除图书记录
    book_to_delete = books_ids[2:]
    deleted = models.execute_kw(db_name, user_id, password, 'mylibrary.book', 'unlink', [book_to_delete])
    print('Books unlinked:', deleted)
else:
    print("Wrong credentials")