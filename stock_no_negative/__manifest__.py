# © 2015-2016 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).



{
    'name': "Stock Disallow Negative",

    'summary': """
        Disallow negative stock levels by default""",

    'description': """
        Disallow negative stock levels by default
    """,

    'author': "Akretion,Odoo Community Association (OCA)",
    'website': "http://www.akretion.com",
    'license': 'AGPL-3',

    'category': 'Inventory, Logistic, Storage',
    'version': '0.1',
    'depends': ['stock'],

    'data': [
        'views/product.xml'

    ],
    'installable': True,
    'auto_install': False,

}
