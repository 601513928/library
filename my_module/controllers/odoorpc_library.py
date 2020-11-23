import odoorpc



db_name = 'library'
user_name = 'admin'
password = 'admin'
#对服务器端的连接
odoo = odoorpc.ODOO('localhost', port=8069)
odoo.login(db_name, user_name, password)

#用户信息
user = odoo.env.user
print(user.name) 
print(user.company_id.name)
print(user.email)

BookModel = odoo.env['mylibrary.book']
search_domain = ['|', ['name', 'ilike', 'odoo'], ['name', 'ilike', 'sql']]
books_ids = BookModel.search(search_domain, limit=5)
for book in BookModel.browse(books_ids):
    print(book.name, book.date_release)

book_id = BookModel.create({'name': 'Test book2', 'state': 'draft'})
book = BookModel.browse(book_id)
print("Book state before make_available:", book.state)
book.make_available()
book = BookModel.browse(book_id)
print("Book state before make_available:", book.state)

#原生的语法
# books_info = odoo.execute('mylibrary.book', 'search_read', [['name', 'ilike', 'odoo']], ['name', 'date_release'])
# print(books_info)