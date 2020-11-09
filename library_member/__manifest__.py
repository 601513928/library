{
    'name': 'Library Members',
    'description': 'Manage people who will be able to borrow books.',
    'author': 'Alan Hou',
    'depends': ['library_app', 'mail'],
    'data':[
        'security/ir.model.access.csv',
        'views/book_view.xml',
        'views/library_menu.xml',
        'views/member_view.xml',
        'views/book_list_template.xml'
    ],
    'application': False, 
}