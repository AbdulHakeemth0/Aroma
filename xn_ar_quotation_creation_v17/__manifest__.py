

{
    "name": "Quotation Creation",
    "summary": "This module enable the revision in quotation and sale order",
    "version": "1.0",
    "license": "AGPL-3",
    "author":"Xeten Systems and Solutions",
    "company":'Xeten Systems and Solutions',
    "depends": [
        "base","product","sale","account","stock","xn_aroma_v17","xn_aroma_varient_creation_v17",
    ],
    "data": [
        "views/xn_product_category.xml",
        "views/xn_quotation_creation.xml",
        # "views/order_view.xml",
        "wizard/xn_quotation_wiz.xml",

    ],
    "installable": True,
    'auto_install': False,

}
