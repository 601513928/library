from odoo import models, fields, api
from odoo.addons import decimal_precision as dp
from datetime import timedelta
from odoo.tools.translate import _
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)
#新会员模型
class LibraryMember(models.Model):
    _name = 'mylibrary.member'
    _inherits = {'res.partner': 'partner_id'}
    partner_id = fields.Many2one(
        'res.partner',
        ondelete='cascade'
    )

    date_start = fields.Date('Member Since')
    date_end = fields.Date('Termination Date')
    member_number = fields.Char()
    date_of_birth = fields.Date('Date of birth')
#存档的抽象模型
class BaseArchive(models.AbstractModel):
    _name = 'base.archive'
    active = fields.Boolean(default=True)
    def do_archive(self):
        for record in self:
            record.active = not record.active

#伙伴模型
class ResPartner(models.Model):
    _inherit = 'res.partner'
    published_book_ids = fields.One2many(
        'mylibrary.book',
        'publisher_id',
        string="Published Books"
    )

    authored_book_ids = fields.Many2many(
        'mylibrary.book',
        string='Authored Books',
        #relation='library_book_res_partner_rel' #optional
    )
    count_books = fields.Integer('Number of Authored Books',
        compute='_compute_count_books')
    
    @api.depends('authored_book_ids')
    def _compute_count_books(self):
        for r in self:
            r.count_books = len(r.authored_book_ids)

class LibraryBookIssues(models.Model):
    _name = 'book.issue'

    book_id = fields.Many2one('mylibrary.book', required=True)
    submitted_by = fields.Many2one('res.users')
    issue_description = fields.Text()

#自己定义的图书模型
class LibraryBook(models.Model):
    _name = 'mylibrary.book'
    _description = "MyLibrary Book"
    _order = 'date_release desc, name'
    _rec_name = 'short_name'
    _inherit = ['base.archive']

    manager_remarks = fields.Text('Manager Remarks')

    #防止非Librarian成员修改manager_remarks
    @api.model
    def create(self, values):
        if not self.user_has_groups('my_library.group_librarian'):
            if  'manager_remarks' in values:
                raise UserError(
                    'You are not allowed to modify '
                    'manager_remarks'
            )
        return super(LibraryBook, self).create(values)
    
    @api.multi
    def write(self, values):
        if not self.user_has_groups('my_library.group_librarian'):
            if 'manager_remarks' in values:
                raise UserError(
                    'You are not allowed to modify '
                    'manager_remarks'
            )
        return super(LibraryBook, self).write(values)
    #数据库约束
    _sql_constraints = [
        ('name_uniq',
        'UNIQUE(name)',
        'Book title must be unique.'
        ),
        (
            'positive_page',
            'CHECK(pages>0)',
            'No. of pages must be positive'
        )
    ]
    #图书的状态
    state = fields.Selection(
        [
            ('draft', 'Unavailable'),
            ('available', 'Available'),
            ('borrowed', 'Borrowed'),
            ('lost', 'Lost')
        ],
        string='State',
        default='draft'
    )
    short_name = fields.Char('Short Title', translate=True, index=True)
    notes = fields.Text('Internal Notes')
    # state = fields.Selection(
    #     [('draft', 'Not Available'),
    #     ('available', 'Available'),
    #     ('lost', 'Lost'),],
    #     'State',
    #     default="draft"
    # )
    description = fields.Html('Descripiton', sanitize=True, strip_style=False)
    cover = fields.Binary('Book Cover')
    out_of_print = fields.Boolean('Out of Print?')
    date_updated = fields.Datetime('Last Updated')
    pages = fields.Integer('Number of Pages',
        groups='base.group_user',
        states={'lost': [('readonly', True)]},
        help='Total book page count', company_dependent=False
    )
    reader_rating = fields.Float(
        'Reader Average Rating',
        digits=(14, 4),  #optional precision (total, decimals),
    )
    name = fields.Char('Title', required=True)
    date_release = fields.Date('Release Date')
    isbn = fields.Char('ISBN')
    old_edition = fields.Many2one('mylibrary.book', string="Old Edition")
    image = fields.Binary(attachment=True)
    html_description = fields.Html()
    book_issue_id = fields.One2many('book.issue', 'book_id')
    #图书与作者之间的对应
    author_ids = fields.Many2many(
        'res.partner',
        string='Authors'
    )
    #金额
    cost_price = fields.Float(
        'Book Cost', dp.get_precision('Book Price')
    )
    #货币类型
    currency_id = fields.Many2one(
        'res.currency', string='Currency'
    )
    #添加货币字段来存储数额
    retail_price = fields.Monetary(
        'Retail Price',
        #optional: currency_field='currency_id',
    )
    #图书出版社
    publisher_id = fields.Many2one(
        'res.partner',
        string='Publisher',
        #optional:
        ondelete='set null',
        context={},
        domain=[],
    )

    #通过关联字段来使用关联字段中的城市字段
    publisher_city = fields.Char('Publisher City',
        related='publisher_id.city',
        readonly=True
    )

    #图书的分类
    category_id = fields.Many2one('mylibrary.book.category')

    #加入一个字段以及支持它的逻辑方法
    age_days = fields.Float(
        string='Days Since Release',
        compute='_compute_age',
        inverse='_inverse_age',
        search='_search_age',
        store=False,
        compute_sudo=False
    )
    #引用模型
    ref_doc_id = fields.Reference(
        selection='_referencable_models',
        string='Reference Document'
    )
    @api.model
    def _referencable_models(self):
        models = self.env['ir.model'].search([
            ('field_id.name', '=', 'message_ids')
        ])
        return [(x.model, x.name) for x in models]

    @api.depends('date_release')
    def _compute_age(self):
        today = fields.Date.today()
        for book in self.filtered('date_release'):
            delta = today - book.date_release
            book.age_days = delta.days

    def _inverse_age(self):
        today = fields.Date.today()
        for book in self.filtered('date_release'):
            d = today - timedelta(days=book.age_days)
            book.date_release = d

    def _search_age(self, operator, value):
        today = fields.Date.today()
        value_days = timedelta(days=value)
        value_date = today - value_days

        operator_map = {
            '>': '<', '>=': '<=',
            '<': '>', '<=': '>=',
        }
        new_op =  operator_map.get(operator, operator)
        return [('date_release', new_op, value_date)]
    def name_get(self):
        result = []
        for record in self:
            rec_name = "%s (%s)" % (record.name, record.date_release)
            result.append((record.id, rec_name))
        return result
    #Python代码约束
    @api.constrains('date_release')
    def _check_release_date(self):
        for record in self:
            if record.date_release and record.date_release > fields.Date.today():
                raise models.ValidationError('Release date must be in the past')
    #是否允许状态转换
    @api.model
    def is_allowed_transition(self, old_state, new_state):
        allowed = [('draft', 'available'),
                    ('available', 'borrowed'),
                    ('borrowed', 'available'),
                    ('available','lost'),
                    ('borrowed', 'lost'),
                    ('lost', 'available')
        ]
        return (old_state, new_state) in allowed
    @api.multi
    def change_state(self, new_state):
        for book in self:
            if book.is_allowed_transition(book.state, new_state):
                book.state = new_state
            else:
                msg = _('Moving from %s to %s is not allowed') % (book.state, new_state)  # _()函数用于标记字符串可以翻译
                raise UserError(msg)
    def make_available(self):
        self.change_state('available')
    def make_borrowed(self):
        self.change_state('borrowed')

    def make_lost(self):
        self.change_state('lost')
    
    #搜索所有的图书会员
    @api.model
    def get_all_library_member(self):
        library_member_model = self.env['mylibrary.member']
        member_list = library_member_model.search([])
        return member_list

    #更新图书的date_updated 字段
    #第一种实现方法
    @api.multi
    def change_update_date(self):
        self.ensure_one()
        self.date_updated = fields.Datetime.now()
    #第二种实现方法
    @api.multi
    def change_update_date(self):
        self.ensure_one()
        self.update({
            'date_updated': fields.Datetime.now(),
            # 'another_field': 'value'
        })
    
    #查询图书
    def find_book(self):
        domain = [
            '|',
            '&', ('name', 'ilike', 'Book Name'),
            ('category_id.name', 'ilike', 'Category Name'),
            '&', ('name', 'ilike', 'Book Name 2'),
            ('category_id.name', 'ilike', 'Category Name 2')
        ]

        books = self.search(domain)
    #提取含有多名作者的图书
    @api.multi
    def books_with_multiple_authors(self, all_books):
        def predicate(book):
            if len(book.author_ids) > 1:
                return True
                return False
        #使用lambda
        #return all_books.filter(lambda b: len(b.author_ids) > 1)
        return all_books.filter(predicate)

    #从图书集中获取作者的名称
    @api.model
    def get_author_names(self, books):
        return books.mapped('author_ids.name')

    #对记录集排序
    @api.model
    def sort_books_by_date(self, books):
        return books.sorted(key="release_date") #options reverse=True 逆向排序
    
    @api.multi
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        args = [] if args is None else args.copy()
        if not(name == '' and operator == 'ilike'):
            args +=['|', '|',
                ('name', operator, name),
                ('isbn', operator, name),
                ('author_ids.name', operator, name)
            ]
        return super(LibraryBook, self)._name_search(
            name=name, args=args, operator=operator,
            limit=limit, name_get_uid=name_get_uid
        )

    @api.model
    def _get_average_cost(self):
        grouped_result = self.read_group(
            [('cost_price', '!=', False)],
            ['category_id', 'cost_price:avg'],
            ['category_id']
        )
        return grouped_result

    def get_average_cost(self):
        return self._get_average_cost()
    
    #为所有图书的价格增加10
    @api.model
    def _update_book_price(self):
        all_books = self.search([])
        for book in all_books:
            book.cost_price += 10
    
    #为指定的分类图书增家指定价格
    @api.model
    def update_book_price(self, category, amount_to_increase):
        print("Categroy:----------------",category)
        category_books = self.search([('category_id', '=', category)])
        for book in category_books:
            book.cost_price += amount_to_increase

    #让普通用户来借书
    def book_rent(self):
        self.ensure_one()
        if self.state != 'available':
            raise UserError(_('Book is not available for renting'))
        rent_as_superuser = self.env['mylibrary.book.rent'].sudo()
        rent_as_superuser.create({
            'book_id': self.id,
            'borrower_id': self.env.user.partner_id.id,
        })
    
    #图书遗失
    def make_lost(self):
        self.ensure_one()
        self.state = 'lost'
        if not self.env.context.get('avoid_deactivate'):
            self.active = False
    #获取用户保留某本书的平均天数
    def average_book_occupation(self):
        sql_query = """
            SELECT
              lb.name,
              avg((EXTRACT(epoch from age(return_date, rent_date)) / 86400))::int 
            FROM
              mylibrary_book_rent AS lbr
            JOIN
              mylibrary_book as lb ON lb.id = lbr.book_id
            WHERE lbr.state = 'returned'
                GROUP BY lb.name;"""
        self.env.cr.execute(sql_query)
        result = self.env.cr.fetchall()
        _logger.info("Average book occupation: %s", result)



    # def post_to_webservice(self, data):
    #     try:
    #         req = requests.post('http://my-test-service.com', data=data, timeout=10)
    #         content = req.json()
    #     except IOError:
    #         error_msg = _("Something went wrong during data submission")
    #         raise UserError(error_msg)
    #     return content

