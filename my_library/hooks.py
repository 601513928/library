from odoo import fields, api, SUPERUSER_ID

#init钩子
#pre_init_hook : 这个钩⼦会在开始安装模块时触发。它与post_init_hook正好相反， 会在当前模块安装前触发。
#uninstall_hook :这个钩⼦会在你卸载该模块时触发。它多⽤于模块需要垃圾回收机 制时。
def add_book_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    book_data1 = {'name': 'Book1', 'date_release': fields.Date.today()}
    book_data2 = {'name': 'Book2', 'date_release': fields.Date.today()}
    env['mylibrary.book'].create([book_data1, book_data2])