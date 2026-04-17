# -*- coding: utf-8 -*-
{
    'name': "Aroma Varient Creation",

    'summary': """
        For Creating Aroma Varients""",

    'description': """
        For Creating Aroma Varients
    """,

    'author': "Netex Systems and Solutions",

    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','product'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
}