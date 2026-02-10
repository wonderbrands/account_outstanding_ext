{
    'name': 'Invoice Outstanding Widget Extended',
    'version': '18.0.1.0.0',
    'category': 'Accounting',
    'depends': ['account'],
    'data': [],
    'assets': {
        'web.assets_backend': [ # 'web.assets_qweb' ya no existe
            'account_outstanding_ext/static/src/xml/account_payment_extended.xml',
        ],
    },
    'installable': True,
    'license': 'LGPL-3',
}