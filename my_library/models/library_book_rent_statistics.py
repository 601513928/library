from odoo import models, fields, api, tools

class LibraryBookRentStatistics(models.Model):
    _name = 'mylibrary.book.rent.statistics'
    _auto = False

    book_id = fields.Many2one('mylibrary.book', 'Book', readonly=True)
    rent_count = fields.Integer(string="Times borrowed", readonly=True)
    average_occupation = fields.Integer(string="Average Occupation (DAYS)", readonly=True)

    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        query = """
        CREATE OR REPLACE VIEW mylibrary_book_rent_statistics AS
        (
            SELECT
              min(lbr.id) as id,
              lbr.book_id as book_id,
              count(lbr.id) as rent_count,
              avg((EXTRACT(epoch from age(return_date, rent_date)) / 86400))::int as average_occupation
            FROM
              mylibrary_book_rent AS lbr
            JOIN
              mylibrary_book as lb ON lb.id = lbr.book_id
            WHERE lbr.state = 'returned'
            GROUP BY lbr.book_id
        );
        """
        self.env.cr.execute(query)