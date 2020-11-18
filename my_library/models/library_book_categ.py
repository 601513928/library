from odoo import models, fields, api

class BookCategory(models.Model):
    _name = 'mylibrary.book.category'


    name = fields.Char('Category')
    description = fields.Text('Description')


    _parent_store = True
    _parent_name = 'parent_id'
    parent_id = fields.Many2one(
        'mylibrary.book.category',
        string='Parent Category',
        ondelete='restrict',
        index=True
    )

    child_ids = fields.One2many(
        'mylibrary.book.category',
        'parent_id',
        string='Child Categories'
    )
    #在等级树中添加索引并存储
    parent_path = fields.Char(index=True)

    @api.constrains('parent_id')
    def _check_hierarchy(self):
        if not self._check_recursion():
            raise models.ValidationError('Error! You cannot create recursive categories.')

    #创建子分类的方法
    def create_categories(self):
        categ1 = {
            'name': 'Child category 1',
            'description': 'Description for child 1'
        }
        categ2 = {
            'name': 'Child category 2',
            'description': 'Description for child 2'
        }
        parent_category_val = {
            'name': 'Parent category',
            'email': 'Description for parent category',
            'child_ids':[
                (0, 0, categ1),
                (0, 0, categ2),
            ]
        }
        record = self.env['mylibrary.book.category'].create(parent_category_val)

