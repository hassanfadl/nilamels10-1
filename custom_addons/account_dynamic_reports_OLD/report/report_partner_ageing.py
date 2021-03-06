# -*- coding: utf-8 -*-

import time
from odoo import api, models, _
from odoo.exceptions import UserError


class InsReportPartnerAgeing(models.AbstractModel):
    _name = 'report.account_dynamic_reports.partner_ageing'

    @api.model
    def render_html(self, docids, data=None):
        if self.env.context.get('from_js'):
            if data.get('js_data'):
                sorted_partner = []
                
                for p in data.get('js_data')[4]:
                    sorted_partner.append(str(p))
                    
                docargs = {'Ageing_data': data.get('js_data')[1],
                             'Filters': data.get('js_data')[0],
                             'Period_Dict': data.get('js_data')[2],
                             'Period_List': data.get('js_data')[3],
#                             'sorted_partner': data.get('js_data')[4]
                             'sorted_partner': sorted_partner
                             }
                return self.env['report'].render('account_dynamic_reports.partner_ageing', docargs)

        docargs = {'Ageing_data': data.get('Ageing_data'),
                             'Filters': data.get('Filters'),
                             'Period_Dict': data.get('Period_Dict'),
                             'Period_List': data.get('Period_List'),
                             'sorted_partner': data.get('sorted_partner')
                             }
        return self.env['report'].render('account_dynamic_reports.partner_ageing', docargs)
