from odoo import http
from odoo.http import request
class Hello(http.Controller):

    @http.route('/helloworld', auth="public", website=True)
    def helloworld(self, **kwgrgs):
        return request.render('library_website.helloworld')
    #使用CMS动态创建网页，在路由中使用模板名
    @http.route('/hellocms/<page>', auth="public")
    def hello(self, page, **kwargs):
        return http.request.render(page)