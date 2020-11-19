{
    'name' : "My Library",
    'summary': "Manage books easily",
    'description': """Long description""",
    'author': 'CJH',
    'website': 'http://www.example.com',
    'category': 'Uncategorized',
    'version':  '12.0.1',
    'depends': [
        'base',
        'decimal_precision',
        'website',
        'web',
    ],
    'data':[
        
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/library_book.xml',
        'views/library_category.xml',
        'views/library_author.xml',
        'views/library_member.xml',
        'views/library_rent.xml',
        'views/library_rent_wizard.xml',
        'views/library_return.xml',
        'views/library_book_rent_statistics.xml',
        'data/data.xml',
        'data/demo.xml',
        'views/templates.xml',
    ],
    'demo':[

    ],
    'post_init_hook': 'add_book_hook',
    'application': True,

}