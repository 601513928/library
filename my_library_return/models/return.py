from odoo import fields, models, api, exceptions

#继承图书模型，加入还书功能（字段）
class LibraryBook(models.Model):
    _inherit = 'mylibrary.book'
    
    date_return = fields.Date('Date to return')
    
#重写make_borrowed方法，添加还书日期字段
    def make_borrowed(self):
        day_to_borrow = self.category_id.max_borrow_days or 10
        self.date_return = fields.Date.today() = timedelta(days=day_to_borrow)
        return super(LibraryBook, self).make_borrowed()
#重写make_available方法，添加还书状态字段
    def make_available(self):
        self.date_return = False
        return super(LibraryBook, self).make_available()

#继承图书分类
class LibraryBookCategory(models.Model):
    _inherit = 'mylibrary.book.category'
    max_borrow_days = fields.Integer(
        'Maximum borrow days',
        help="For how many days book can be borrowed",
        default=10
    )