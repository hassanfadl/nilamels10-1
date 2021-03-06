# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'GTS COA',
    'version' : '1.1',
    'summary': 'GTS COA',
    'author' : "Geo Technosoft",
    'sequence': 30,
    'description': """ Chart of Accounts with hierarchy.
This module create parent and child relation in account""",
    'category' : 'Accounting & Finance',
    'price': 19.99,
    'currency':'EUR',
    'license': 'OPL-1',
    'website': 'www.geotechnosoft.com',
    'depends' : ['account', 'account_accountant'],
    'data': [
        'data/report_paperformat.xml',
        'views/account_account_view.xml',
        'views/report_trialbalance.xml',
        'views/report_financial.xml',
        'report/gts_coa_reports.xml',
        'wizard/account_report_trial_balance_view.xml',
        'wizard/account_financial_report_view.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
