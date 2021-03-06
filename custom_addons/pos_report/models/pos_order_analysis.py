# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging
from datetime import timedelta
from functools import partial

import psycopg2

from odoo import api, fields, models, tools, _
from odoo.tools import float_is_zero
from odoo.exceptions import UserError
from odoo.http import request
import odoo.addons.decimal_precision as dp

_logger = logging.getLogger(__name__)




class ReportSaleDetails(models.Model):

    _name = 'report.pos_report.report_order_analysis'


    @api.model
    def get_order_details(self, date_start, date_stop):
        """ Serialise the orders of the day information

        params: date_start, date_stop string representing the datetime of order
        """
	date_start = date_start
	date_stop = date_stop
	print '============get_order_details'
	print date_start,'======333333========date_start'
	print date_stop,'========33333=========date_stop:'
        today = fields.Datetime.from_string(fields.Date.context_today(self))
        if date_start:
            date_start = fields.Datetime.from_string(date_start)
        else:
            # start by default today 00:00:00
            date_start = today

        if date_stop:
            # set time to 23:59:59
            date_stop = fields.Datetime.from_string(date_stop)
        else:
            # stop by default today 23:59:59
            date_stop = today + timedelta(days=1, seconds=-1)

        # avoid a date_stop smaller than date_start
        date_stop = max(date_stop, date_start)

        date_start = fields.Datetime.to_string(date_start)
        date_stop = fields.Datetime.to_string(date_stop)
	print date_start,'======date_start'
	print date_stop,'==========date_stop'
        orders = self.env['pos.order'].search([
            ('date_order', '>=', date_start),
            ('date_order', '<=', date_stop),
            ('state', 'in', ['paid','invoiced','done']),
            ])

	print orders,'============22222=========orders'
        net_sale = 0.0
        margin_percentage = 0
        profit = 0.0
        margin_percentage_round = 0
        order_list = []
        pos_order = {}
        for order in orders:
	    print order,'===22222============order'		
            for line in order.lines:
                net_sale = line.qty * line.price_unit
                total_disc = line.qty * line.discount
                total_standard_price = line.qty * line.product_id.standard_price
                profit = net_sale - total_disc - total_standard_price
                if total_standard_price > 0:
                    margin_percentage =( profit / net_sale )  * 100
                    margin_percentage_round = round(margin_percentage,2)
                pos_order = {
                             'start_date' : date_start,
                             'end_date' : date_stop,
                             'item_name' : line.product_id.name,
                             'qty' : line.qty,
                             'sold_price' : line.price_unit,
                             'discount' : line.discount,
                             'net_sale' : net_sale,
                             'product_cost' : line.product_id.standard_price,
                             'profit' : profit,
                             'profit_margin' : margin_percentage_round,
                             }
                order_list.append(pos_order)
        print order_list,'=====11111111===========order_list'
        return order_list
                
                
                

    @api.multi
    def render_html(self, docids, data=None):
	print self.env.context,'===================self.env.context'
	active_model = self.env.context.get('active_model')
	active_id = self.env.context.get('active_id')
	print active_id,'===============active_id'
	order_analysis_obj = self.env['order.analysis.wizard']
	order_analysis_rec = order_analysis_obj.search([('id','=',active_id)])
	print order_analysis_rec,'==========order_analysis_rec'
        date_start = order_analysis_rec.start_date
        date_stop = order_analysis_rec.end_date
        data = dict(data or {}, date_start=date_start, date_stop=date_stop)
        data.update(pos_order = self.get_order_details(date_start, date_stop))
	print data,'============11111=========data'
        print '=======================1'
        return self.env['report'].render('pos_report.report_order_analysis', data)
