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
from openerp import models, fields, api, _
from datetime import datetime


class wallet_management(models.Model):
    _name = 'wallet.management'

    customer_id = fields.Many2one('res.partner', string='Customers')
    order_id = fields.Many2one('pos.order', string='Order')
    type = fields.Selection([('change','Change'),('return','Return')],string="Type")
    debit = fields.Float("Debit")
    credit = fields.Float("Credit")
    cashier_id = fields.Many2one('res.users',string='Cashier')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: