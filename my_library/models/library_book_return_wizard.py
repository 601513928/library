from odoo import models, fields, api

#归还图书的向导
class LibraryReturnWizard(models.TransientModel):
    _name = 'mylibrary.return.wizard'
    borrower_id = fields.Many2one('res.partner', string="Member")
    book_ids = fields.Many2many('mylibrary.book',string="Books")

    def books_returns(self):
        rentModel = self.env['mylibrary.book.rent']
        for rec in self:
            rentModels = rentModel.search([
                ('state', '=', 'ongoing'),
                ('book_id', 'in', rec.book_ids.ids),
                ('borrower_id', '=', rec.borrower_id.id)
            ])
        for rent in rentModels:
            rent.book_return()

    @api.onchange('borrower_id')
    def onchange_member(self):
        rentModel = self.env['mylibrary.book.rent']
        books_on_rent = rentModel.search([
            ('state', '=', 'ongoing'),
            ('borrower_id', '=', self.borrower_id.id)
        ])
        self.book_ids = books_on_rent.mapped('book_id')