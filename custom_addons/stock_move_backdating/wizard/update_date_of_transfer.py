# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import time

def check_date(date):
    now = fields.Datetime.now()
    if date > now:
        raise UserError(
            _("You can not process an actual "
              "movement date in the future."))
              
class UpdateDateTransfer(models.TransientModel):
    _name = 'update.date.transfer'

    date_done = fields.Datetime(string='Date of Transfer')
    
    @api.multi
    def process(self):
        if self._context.get('active_ids',False):
            picking_obj = self.env['stock.picking']
            account_move = self.env['account.move']
            pickings = picking_obj.browse(self._context['active_ids'])
            force_period_date=self.date_done
            for picking in pickings:
                picking.pack_operation_ids.write({'date': force_period_date })
                picking.move_lines.write({'date': force_period_date,'expected_date': force_period_date})
                picking.write({'date_done': force_period_date })

                account_move = account_move.search([('ref','=',picking.name)])
                if not account_move:
                    raise UserError(_("Journal Entry not Found"))

                account_move.write({'date': force_period_date })
                # for move in picking.move_lines:
                #     domain = [('product_id','=',move.product_id.id),('move_id.journal_id','=',move.product_id.categ_id.property_stock_journal.id),('journal_id','=',move.product_id.categ_id.property_stock_journal.id),('move_id.ref','=',picking.name)]
                #     account_move_lines = self.env['account.move.line'].search(domain)
                #     print'account_move_lines',account_move_lines
                #     if not account_move_lines:
                #         raise UserError(
                #     _("Journal Entry not Found"))
                #     account_move_lines[0].move_id.write({'date': force_period_date })

        return True