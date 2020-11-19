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

        #Python返回一个python字段，包含warning和domain
        result = {
            'domain': {
                'book_ids':[ ('id', 'in', self.book_ids.ids)]
            }
        }
        late_domain = [
            ('book_id', 'in', self.book_ids.ids),
            ('return_date', '<', fields.Date.today())
        ]
        late_books = rentModel.search(late_domain)
        if late_books:
            message = ('Warn the member that the following'
                        'books are late:\n')
            titles = late_books.mapped('book_id.name')
            result['warning'] = {
                'title': 'Late books',
                'message': message + '\n'.join(titles)
            }
        return result
    
    #非管理员归还图书
    # @api.multi
    # def return_all_books(self):
    #     self.ensure_one()
    #     wizard = self.env['mylibrary.return.wizard']

    #     values = {
    #         'borrower_id': self.env.user.partner_id.id,
    #     }

    #     specs = wizard._onchange_spec()
    #     updates = wizard.onchange(values, ['borrower_id'], specs)

    #     value = updates.get('value', {})
    #     for name, val in value.items():
    #         if isinstance(val, tuple):
    #             value[name] = val[0]
    #     values.update(value)
    #     wiz = wizard.create(values)
    #     return wiz.sudo().books_returns()


        