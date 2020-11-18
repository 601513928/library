from odoo import models, fields

class LibraryBookRent(models.Model):
    _name = 'mylibrary.book.rent'

    book_id = fields.Many2one('mylibrary.book', 'Book', required=True)
    borrower_id = fields.Many2one('res.partner', 'Borrower', required=True)
    state = fields.Selection(
        [
            ('ongoing', 'Ongoing'),
            ('returned', 'Returned'),
            ('lost', 'Lost')
        ],
        'State', default='ongoing',
        required=True
    )
    rent_date = fields.Date(default=fields.Date.today)
    return_date = fields.Date()

    #图书遗失
    def book_lost(self):
        self.ensure_one()
        self.state = 'lost'
        book_with_different_context = self.book_id.with_context(avoid_deactivate=True)
        book_with_different_context.make_lost()

    #归还图书
    def book_return(self):
        self.ensure_one()
        self.state = 'returned'
        