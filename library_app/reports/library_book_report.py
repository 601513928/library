from odoo import models, fields

#报表类
class BookReport(models.Model):
    _name = 'library.book.report'
    _description = 'Book Report'
    _auto = False

    name = fields.Char('Title')
    publisher_id = fields.Many2one('res.partner')
    date_published = fields.Date()

    def init(self):
        self.env.cr.execute("""
            create or replace view library_book_report as
            (select * from library_book
            where active=True)
        """)