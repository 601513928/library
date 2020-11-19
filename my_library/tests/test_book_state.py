from odoo.tests.common import TransactionCase, tagged
#在所有模块安装之后运行测试用例 at_install 默认在安装完本模块之后立即运行
# @tagged('-at_install', 'post_install')
#自定义标签
#使用 --test-tags=my_custom_tag
#默认 --test-tags=my_library 可以使用模块技术名
@tagged('-standard', 'my_custom_tag')
class TestBookState(TransactionCase):

    def setUp(self, *args, **kwargs):
        super(TestBookState, self).setUp(*args, **kwargs)
        self.test_book = self.env['mylibrary.book'].create({'name': 'Book 1'})
    #需要指定数据库
    def test_button_available(self):
        self.test_book.make_available()
        self.assertEqual(self.test_book.state, 'available', 'Book state should changed to available')

    def test_button_lost(self):
        self.test_book.make_lost()
        self.assertEqual(self.test_book.state, 'lost', 'Book state should changed to lost')