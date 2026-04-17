# -*- coding: utf-8 -*-
{
    'name': "Aroma V11",

    'summary': """
        Netex Aroma Module""",

    'description': """
        Netex Aroma Module
    """,

    'author': "Netex Systems and Solutions",
    'website': "http://www.yourcompany.com",

    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base','sale','account','mrp','stock','sale_stock'],

    'data': [
        # 'report/aroma_invoice_report.xml',
        'report/aroma_invoice_report_main.xml',
        # 'report/aroma_lot_report.xml',
        'report/aroma_lot_report_main.xml',
        'report/aroma_invoice_report_layout.xml',
        'sale/sale_order_view.xml',
        'account/account_invoice_view.xml',
        # 'mrp/mrp_produce_wizard.xml',
    ],

}