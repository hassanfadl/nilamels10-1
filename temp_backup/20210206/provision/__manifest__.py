# -*- coding: utf-8 -*-
{
    'name': "provision",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Mada Solutions Pvt Ltd",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/10.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','purchase','account','stock',
            'direct_sale','sale_commission', 'bi_generic_import','account_reports',
            'account_powersports', 'ledgers_filter_custom'],

    # always loaded
    'data': [
         'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/stock_location_views.xml',
        'views/account_view.xml',
        'views/account_payment_view.xml',
        'views/job_master_view.xml',
        'report/account_invoice.xml',
        'report/report_accountvoucher_account_move.xml',
        'report/report_generalledger.xml',
        'report/payment_report.xml',
        'report/payment_report_templates.xml',
        
        'views/invoice_report.xml',
        'views/report_invoice_inv.xml',
        'views/report_invoice_del.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
#        'demo/demo.xml',
    ],
}