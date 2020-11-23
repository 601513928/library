from odoo import http
from odoo.http import request
from odoo.addons.website.controllers.main import Website
from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.website.models.ir_http import sitemap_qs2dom
import os, re
from openpyxl import Workbook
class Main(http.Controller):

    # def sitemap_books(env, rule, qs):
    #     Books = env['mylibrary.book']
    #     dom = sitemap_qs2dom(qs, '/books', Books._rec_name)
    #     for f int Books.search(dom):
    #         loc - '/books/%s' % slug(f)
    #         if not qs or qs.lower() in loc:
    #             yield{'loc': loc}
    @http.route('/my_library/books', type='http', auth='none')
    def books(self):
        books = request.env['mylibrary.book'].sudo().search([])
        html_result = '<html><body><ul>'
        for book in books:
            html_result += "<li> %s </li>" % book.name
        html_result += "</ul></body></html>"
        return html_result

    @http.route('/my_library/books/json', type="json", auth="none")
    def books_json(self):
        records = request.env['mylibrary.book'].sudo().search([])
        result = records.read(['name'])
        return json.dumps(result)

    @http.route('/my_library/all-books', type='http', auth='public')
    def all_books(self):
        books = request.env['mylibrary.book'].sudo().search([])
        html_result = '<html><body><ul>'
        for book in books:
            html_result += "<li> %s </li>" % book.name
            html_result += '</ul></body></html>'
        return html_result
    @http.route('/my_library/all-books/mark-mine', type='http', auth='public')
    def all_books_mark_mine(self):
        books = request.env['mylibrary.book'].sudo().search([])
        html_result = '<html><body><ul>'
        for book in books:
            if request.env.user.partner_id.id in book.author_ids.ids:
                html_result += "<li><em> <b>%s</b> </em></li>" % book.name
            else:
                html_result += "<li> %s </li>" % book.name
        html_result += '</ul></body></html>'
        return html_result
    @http.route('/my_library/all-books/mine', type='http', auth='user')
    def all_books_mine(self):
        books = request.env['mylibrary.book'].search([
            ('author_ids', 'in', request.env.user.partner_id.ids),
        ])
        html_result = '<html><body><ul>'
        for book in books:
            html_result += "<li> %s </li>" % book.name
        html_result += '</ul></body></html>'
        return html_result

    #传入id查询图书
    @http.route("/my_library/book_details", type='http', auth='none')
    def book_details(self, book_id):
        record = request.env['mylibrary.book'].sudo().browse(int(book_id))
        return u'<html><body><h1>%s</h1>Authors: %s' % (record.name, u', '.join(record.author_ids.mapped('name')) or 'none')
    #注意权限问题，这里只能auth='user'使用,访问数据库
    @http.route("/my_library/book_details/<model('mylibrary.book'):book>", type='http', auth='user')
    def book_details_in_path(self, book, **kwargs):
        print("===============")
        return self.book_details(book.id)

    #返回图书列表
    @http.route('/books', type='http', auth='user', website=True)
    def library_books(self):
        return request.render(
            'my_library.books', {
                'books': request.env['mylibrary.book'].search([]),
            }
        )

    #图书详情页面
    @http.route('/books/<model("mylibrary.book"):book>', type='http',auth='user', website=True)
    def library_books_details(self, book):
        return request.render(
            'my_library.book_detail',{
                'book': book,
            }
        )
    
    #问题页面
    @http.route('/books/submit_issues', type="http", auth="user", website=True)
    def books_issues(self, **post):
        if post.get('book_id'):
            book_id = int(post.get('book_id'))
            issue_description = post.get('issue_description')
            request.env['book.issue'].sudo().create({
                'book_id': book_id,
                'issue_description': issue_description,
                'submitted_by': request.env.user.id
            })
            return request.redirect('/books/submit_issues?submitted=1')
        return request.render('my_library.books_issue_form', {
            'books': request.env['mylibrary.book'].search([]),
            'submitted': post.get('submitted', False)
        })

    def get_file():
        current_path = os.getcwd()
        py_list = []
        path = os.path.join(current_path, 'models')
        filelist = os.listdir(path)
        for filename in filelist:
            de_path = os.path.join(path, filename)
            if os.path.isfile(de_path):
                if de_path.endswith(".py"):
                    py_list.append(de_path)
        return py_list

class WebsiteInfo(Website):
    
    #显示已安装的应用程序
    @http.route('/website/info')
    def website_info(self):
        result = super(WebsiteInfo, self).website_info()
        result.qcontext['apps'] =  result.qcontext['apps'].filtered(lambda x: x.name != 'website')
        return result

