from odoo import models, fields

#临时模型
class LibraryRentWizard(models.TransientModel):
    _name = "mylibrary.rent.wizard"
    
    borrower_id = fields.Many2one('res.partner', string="Borrower")
    book_ids = fields.Many2many('mylibrary.book', string="Books")
    
    def add_book_rents(self):
        rentModel = self.env['mylibrary.book.rent']
        print("+++++++++++++++++++")
        for wiz in self:
            for book in wiz.book_ids:
                rentModel.create({
                    'borrower_id': wiz.borrower_id.id,
                    'book_id': book.id
                })
        members = self.mapped('borrower_id')
        print("===================", members, members.ids)
        action = members.get_formview_action()
        if len(members.ids) > 1:
            action['domain'] = [('id', 'in', tuple(members.ids))]
            action['view_mode'] = 'tree,form'
        return action