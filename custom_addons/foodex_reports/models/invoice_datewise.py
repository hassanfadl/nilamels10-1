# -*- coding: utf-8 -*-
#################################################################################
# Author      : Acespritech Solutions Pvt. Ltd. (<www.acespritech.com>)
# Copyright(c): 2012-Present Acespritech Solutions Pvt. Ltd.
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#################################################################################

from odoo import fields, models, api, _
from odoo.exceptions import Warning
from datetime import date
from collections import OrderedDict


class InvoiceDatewise(models.TransientModel):
    _name = "invoice.datewise"

    date_from = fields.Date(string="Date From", default=date.today())
    date_to = fields.Date(string="Date To", default=date.today())
    state = fields.Selection([
        ('all','All'),
        ('draft','Draft'),
        ('open','Open'),
        ('paid','Paid'),
        ('cancel','Cancel')
    ], default='all')
    partner_ids = fields.Many2many('res.partner', string="Customer")
    location_ids = fields.Many2many('stock.location', string="Location" , domain=[('usage', '=', 'internal')])
    salesman_id = fields.Many2one('res.users', string="Salesman")

    @api.multi
    def action_invoice_datewise_report(self):
        self.clear_caches()
        if self.date_to < self.date_from:
            raise Warning(_('Please enter proper date range.'))
        datas = {
            'model': self._name,
            'docids':self.id,
            'date_from': self.date_from,
            'date_to':self.date_to,
            'partner_ids': self.partner_ids.ids if self.partner_ids else [],
            'location_ids':self.location_ids.ids if self.location_ids else False,
            'salesman_id':self.salesman_id.id if self.salesman_id else False,
            'state':self.state
        }
        return self.env['report'].get_action(self, 'foodex_reports.invoice_datewise_report_template', data=datas)


class ReportInvoiceDatewise(models.AbstractModel):
    _name = 'report.foodex_reports.invoice_datewise_report_template'

    @api.model
    def render_html(self, docids, data=None):
        self.clear_caches()
        domain = [('date_invoice', '>=', data.get('date_from')),('date_invoice', '<=', data.get('date_to')), ('type', '=', 'out_invoice')]
        if data.get('partner_ids'):
            domain.append(('partner_id','in',data.get('partner_ids')))
        if data.get('location_ids'):
            domain.append(('location_id','in',data.get('location_ids')))
        if data.get('salesman_id'):
            domain.append(('user_id', '=', data.get('salesman_id')))
        if data.get('state') != 'all':
            domain.append(('state','=',data.get('state')))
#        invoice_ids = self.env['account.invoice'].sudo().search(domain,order='date_invoice')
        invoice_ids = self.env['account.invoice'].sudo().search(domain,order='number')
        date_lst = []
#        data_dict = {}
        data_dict = OrderedDict()
        total = 0
        if invoice_ids:
            total  = sum(invoice_ids.mapped('amount_total'))
            for each in invoice_ids:
                if each.date_invoice not in date_lst:
                    date_lst.append(each.date_invoice)
            date_lst = sorted(date_lst)
            for each in date_lst:
                inv_ids = invoice_ids.filtered(lambda l:l.date_invoice == each)
                data_dict[each] = inv_ids
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('foodex_reports.invoice_datewise_report_template')
        docids = self.env[data['model']].browse(data['docids'])
        docargs = {
            'doc_ids': docids,
            'doc_model': report.model,
            'docs': docids,
            'data': data_dict if data_dict else False,
            'total':total
        }
        return report_obj.render('foodex_reports.invoice_datewise_report_template', docargs)
