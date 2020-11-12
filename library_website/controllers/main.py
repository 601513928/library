from odoo import http
from odoo.http import request

class Main(http.Controller):
    @http.route('/checkouts', auth='user', website=True)
    def checkouts(self, **kwargs):
        Checkout = request.env['library.checkout']
        checkouts = Checkout.search([])
        return request.render('library_website.index', {'docs': checkouts})

    #借阅明细页面                              #默认值，但此处明确指定
    @http.route('/checkout/<model("library.checkout"):doc>', auth='user', website=True)
    def checkout(self, doc, **kwargs):
        return http.request.render(
            'library_website.checkout',
            {'doc': doc}
        )
    
    