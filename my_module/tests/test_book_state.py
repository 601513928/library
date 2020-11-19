from odoo.tests.common import TransactionCase

class TestBookState(TransactionCase):

    def setUp(self, *args, **kwargs):
        super(TestBookState, self).setUp(*args, **kwargs)
        self.test_book = self.env['ilibrary.book'].create({'name': 'Book 1'})
    
    def test_button_available(self):
        self.test_book.make_available()
        self.assertEqual(self.test_book.state, 'available', 'Book state should changed to available')

    def test_button_lost(self):
        self.test_book.make_lost()
        self.assertEqual(self.test_book.state, 'lost', 'Book state should changed to lost')