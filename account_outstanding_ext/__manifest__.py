{
    'name': 'Invoice Outstanding Widget Extended',
    'version': '15.0.1.0.0',
    'category': 'Accounting',
    'depends': ['account'],
    'data': [],
    'assets': {
        'web.assets_qweb': [
            'account_outstanding_ext/static/src/xml/account_payment_extended.xml',
        ],
    },
    'installable': True,
}