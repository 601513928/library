# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ILibraryBook(models.Model):
    _name = 'ilibrary.book'
    name = fields.Char('Title', required=True)
    date_release = fields.Date('Release Date')
    author_ids = fields.Many2many('res.partner', string="Authors")
    state = fields.Selection(
        [
            ('draft', 'Not Available'),
            ('available', 'Available'),
            ('lost', 'Lost')
        ],
        'State',default="draft"
    )
    color = fields.Integer()

    def make_available(self):
        self.write({'state': 'available'})
    
    def make_lost(self):
        self.write({'state': 'lost'})
# class my_module(models.Model):
#     _name = 'my_module.my_module'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100